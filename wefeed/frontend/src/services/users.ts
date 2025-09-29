import api from '../libs/axios'

export interface RegisterPayload {
  name: string
  email: string
  password: string
  
}

export function registerUser(data: RegisterPayload) {
  return api.post('/users/register/', data)
}

export interface LoginPayload {
  email: string
  password: string
}

export function loginUser(data: LoginPayload) {
  return api.post('/users/login/', data)
}

export function loginWithGoogle(token: string) {
  return api.post('/users/oauth/google/', { token })
}

export function loginWithSSO(ssoToken: string) {
  return api.post('/users/oauth/sso/', { token: ssoToken })
}

export function getUserById(id: number) {
  return api.get(`/users/${id}/`)
}

export interface UpdateUserPayload {
  name?: string
  email?: string
}

export function updateUser(id: number, data: UpdateUserPayload) {
  return api.put(`/users/${id}/update/`, data)
}

export interface ChangePasswordPayload {
  old_password: string
  new_password: string
}

export function changePassword(id: number, data: ChangePasswordPayload) {
  return api.put(`/users/${id}/password/`, data)
}

export interface UploadAvatarPayload {
  avatar: File
}

export function uploadAvatar(id: number, data: UploadAvatarPayload) {
  const formData = new FormData()
  formData.append('avatar', data.avatar)
  return api.put(`/users/${id}/avatar/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

