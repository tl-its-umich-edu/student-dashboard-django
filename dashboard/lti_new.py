import logging
import random
import string
from collections import namedtuple
from typing import Any, Dict

import django.contrib.auth
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import logging, string, random
import urllib.parse
from datetime import datetime
from typing import Mapping, MutableSequence, Union, Any

import django.contrib.auth
from django.contrib.staticfiles import finders

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from pylti1p3.contrib.django import DjangoOIDCLogin, DjangoMessageLaunch, \
    DjangoCacheDataStorage
from pylti1p3.tool_config import ToolConfDict

from dashboard.common.db_util import canvas_id_to_incremented_id
from dashboard.models import Course, CourseViewOption, User as MylaUser

logger = logging.getLogger(__name__)
INSTRUCTOR = 'http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor'
TA = 'http://purl.imsglobal.org/vocab/lis/v2/membership/Instructor#TeachingAssistant'
COURSE_MEMBERSHIP = 'http://purl.imsglobal.org/vocab/lis/v2/membership'
DUMMY_CACHE = 'DummyCache'

# do not require deployment ids if LTI_CONFIG_DISABLE_DEPLOYMENT_ID_VALIDATION is true
class ExtendedDjangoMessageLaunch(DjangoMessageLaunch):
    def validate_deployment(self):
        if settings.LTI_CONFIG_DISABLE_DEPLOYMENT_ID_VALIDATION:
            return self

        return super().validate_deployment()

def lti_error(error_message: Any) -> JsonResponse:
    """
    Log an error message and return a JSON response with HTTP status 500.

    :param error_message: `Any` type is allowed so objects may be used
    :return: JsonResponse, with status 500
    """
    logger.error(f'LTI error: {error_message}')
    return JsonResponse({'lti_error': f'{error_message}'}, status=500)


class LTIException(Exception):
    def __init__(self, config,
                 message='An error occurred processing the LTI request.'):
        self.lti_error = LTIError(config)
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'({self.lti_error}) -> "{self.message}"'


def get_tool_conf():
    lti_config = settings.LTI_CONFIG

    try:
        config = ToolConfDict(lti_config)
    except Exception as error:
        return error

    # There should be one key per platform
    # and the name relay on platforms generic domain not institution specific
    platform_domain = list(lti_config.keys())[0]
    platform_config = lti_config[platform_domain][0]
    client_id = platform_config['client_id']

    try:
        with open(platform_config.get(
                'private_key_file', '/secrets/private.key'),
                'r') as private_key_file:
            config.set_private_key(
                platform_domain, private_key_file.read(), client_id)

        with open(platform_config.get(
                'public_key_file', '/secrets/public.key'),
                'r') as public_key_file:
            config.set_public_key(
                platform_domain, public_key_file.read(), client_id)

    except OSError as error:
        return error

    return config


def is_config_valid(config: ToolConfDict):
    if isinstance(config, ToolConfDict):
        logger.info('LTI configuration valid.')
        return True
    else:
        logger.error(f'Invalid LTI configuration: "{config}"')
        return False


def generate_jwks() -> Dict[str, list]:
    config = get_tool_conf()
    if not is_config_valid(config):
        raise LTIException(config)
    return config.get_jwks()


def get_jwks(_: Any) -> JsonResponse:
    """
    Return JWKS generated by `pylti1p3`, based on public key

    :param _: Django passes a Request object, but this method doesn't use it.
    :return: `JsonResponse` containing JWKS or error message.
    """
    try:
        jwks = generate_jwks()
    except LTIException as e:
        return e.lti_error.response_json()

    return JsonResponse(jwks)


def generate_config_json(request: HttpRequest) -> \
        Union[HttpResponse, JsonResponse]:
    config = get_tool_conf()
    if not is_config_valid(config):
        return lti_error(f'Invalid LTI configuration: "{config}"')

    parameters = {
        'timestamp': datetime.now().isoformat(),
        'host': request.get_host(),
        'base_url': urllib.parse.urlunsplit(
            [request.scheme, request.get_host()] + 3 * ['']),
        'login_url_suffix': reverse('login'),
        'launch_url_suffix': reverse('launch'),
        'jwks_url_suffix': reverse('get_jwks'),
    }

    template_path: str
    if settings.LTI_CONFIG_TEMPLATE_PATH is not None:
        template_path = settings.LTI_CONFIG_TEMPLATE_PATH
    else:
        template_path = finders.find(
            'config/lti_config_template.json')

    logger.debug(f'template_path: "{template_path}"')

    template_contents: str
    try:
        with open(template_path, 'r') as template_file:
            template_contents = template_file.read()
    except OSError as error:
        return lti_error('Error reading LTI template file '
                         f'"{template_path}": ({error})')

    config_json: str
    try:
        config_json = template_contents % parameters
    except KeyError as error:
        return lti_error('Error filling in LTI template from '
                         f'"{template_path}": ({error})')

    return HttpResponse(config_json, content_type='application/json')


def get_cache_config():
    CacheConfig = namedtuple('CacheConfig', ['is_dummy_cache', 'launch_data_storage', 'cache_lifetime'])
    is_dummy_cache = DUMMY_CACHE in settings.DB_CACHE_CONFIGS['BACKEND']
    launch_data_storage = DjangoCacheDataStorage(cache_name='default') if not is_dummy_cache else None
    cache_ttl = settings.DB_CACHE_CONFIGS['CACHE_TTL']
    cache_lifetime = cache_ttl if cache_ttl else 7200
    return CacheConfig(is_dummy_cache, launch_data_storage, cache_lifetime)


def check_if_instructor(roles, username, course_id):
    if INSTRUCTOR in roles:
        logger.info(f'user {username} is Instructor in the course {course_id}')
        return True
    return False


def course_user_roles(roles, username):
    user_membership_roles = set([role for role in roles if role.find(COURSE_MEMBERSHIP) == 0])
    if not user_membership_roles:
        logger.info(f'User {username} does not have course membership roles, must be admin {roles}')
    elif INSTRUCTOR in user_membership_roles and TA in user_membership_roles:
        logger.info(f'User {username} is a {TA} in the course')
        user_membership_roles.remove(INSTRUCTOR)
    return user_membership_roles


def short_user_role_list(roles):
    return [role.split('#')[1] for role in roles]


def extract_launch_variables_for_tool_use(request, message_launch):
    launch_data = message_launch.get_launch_data()
    logger.debug(f'lti launch data {launch_data}')
    custom_params = launch_data['https://purl.imsglobal.org/spec/lti/claim/custom']
    logger.debug(f'lti_custom_param {custom_params}')
    if not custom_params:
        raise Exception(
            f'You need to have custom parameters configured on your LTI Launch. Please see the LTI installation guide on the Github Wiki for more information.'
        )
    course_name = launch_data['https://purl.imsglobal.org/spec/lti/claim/context']['title']
    roles = launch_data['https://purl.imsglobal.org/spec/lti/claim/roles']
    username = custom_params['user_username']
    course_id = custom_params['canvas_course_id']
    canvas_course_long_id = canvas_id_to_incremented_id(course_id)
    canvas_user_id = custom_params['canvas_user_id']
    canvas_user_long_id = canvas_id_to_incremented_id(canvas_user_id)
    if 'email' not in launch_data.keys():
        logger.info('Possibility that LTI launch by Instructor/admin becoming Canvas Test Student')
        error_message = 'Student view is not available for My Learning Analytics.'
        raise Exception(error_message)

    email = launch_data['email']
    first_name = launch_data['given_name']
    last_name = launch_data['family_name']
    full_name = launch_data['name']
    user_sis_id = launch_data['https://purl.imsglobal.org/spec/lti/claim/lis']['person_sourcedid']

    # Add user to DB if not there; avoids Django redirection to login page
    try:
        user_obj = User.objects.get(username=username)
    except User.DoesNotExist:
        password = ''.join(random.sample(string.ascii_letters, settings.RANDOM_PASSWORD_DEFAULT_LENGTH))
        user_obj = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
    user_obj.backend = 'django.contrib.auth.backends.ModelBackend'
    django.contrib.auth.login(request, user_obj)
    user_roles = course_user_roles(roles, username)
    is_instructor = check_if_instructor(user_roles, username, course_id)

    try:
        Course.objects.get(canvas_id=course_id)
    except ObjectDoesNotExist:
        if is_instructor or user_obj.is_staff:
            Course.objects.create(id=canvas_course_long_id, canvas_id=course_id, name=course_name)
            CourseViewOption.objects.create(course_id=canvas_course_long_id)
        if is_instructor:
            MylaUser.objects.create(name=full_name, sis_name=username,
                                    course_id=canvas_course_long_id,
                                    user_id=canvas_user_long_id, sis_id=user_sis_id,
                                    enrollment_type=MylaUser.ENROLLMENT_TYPES.TeacherEnrollment)
    return course_id


@csrf_exempt
def login(request):
    config = get_tool_conf()
    if not is_config_valid(config):
        return lti_error(config)
    target_link_uri = request.POST.get('target_link_uri', request.GET.get('target_link_uri'))
    if not target_link_uri:
        error_message = 'LTI Login failed due to missing "target_link_uri" param'
        return lti_error(error_message)
    CacheConfig = get_cache_config()
    oidc_login = DjangoOIDCLogin(request, config, launch_data_storage=CacheConfig.launch_data_storage)
    return oidc_login.enable_check_cookies().redirect(target_link_uri)


@require_POST
@csrf_exempt
def launch(request):
    config = get_tool_conf()
    if not is_config_valid(config):
        return lti_error(config)
    CacheConfig = get_cache_config()
    message_launch = ExtendedDjangoMessageLaunch(request, config, launch_data_storage=CacheConfig.launch_data_storage)
    if not CacheConfig.is_dummy_cache:
        # fetch platform's public key from cache instead of calling the API will speed up the launch process
        message_launch.set_public_key_caching(CacheConfig.launch_data_storage,
                                              cache_lifetime=CacheConfig.cache_lifetime)
    else:
        logger.info('DummyCache is set up, recommended atleast to us Mysql DB cache for LTI advantage services')

    try:
        course_id = extract_launch_variables_for_tool_use(request, message_launch)
    except Exception as e:
        return lti_error(e)

    url = reverse('courses', kwargs={'course_id': course_id})
    return redirect(url)
