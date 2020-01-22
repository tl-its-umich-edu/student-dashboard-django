import { useEffect } from 'react'
import useSetUserSettingGQL from './useSetUserSettingGQL'
import isEqual from 'lodash.isequal'
import { createUserSettings } from '../util/assignment'
import { loadedWithoutError } from '../util/data'

const noUserSetting = data => !data.course.currentUserDefaultSelection

const isUserSettingChanged = (userSetting, data) => {
  return !isEqual(
    userSetting,
    JSON.parse(data.course.currentUserDefaultSelection.defaultViewValue)
  )
}

const useSaveUserSetting = ({ loading, error, courseId, userSetting, data }) => {
  const { saveUserSetting, mutationLoading, mutationError } = useSetUserSettingGQL()

  useEffect(() => {
    if (loadedWithoutError(loading, error)) {
      if (noUserSetting(data) || isUserSettingChanged(userSetting, data)) {
        saveUserSetting(
          createUserSettings(courseId, 'assignmentv2', userSetting)
        )
      }
    }
  }, [JSON.stringify(userSetting)])

  return [mutationLoading, mutationError]
}

export default useSaveUserSetting
