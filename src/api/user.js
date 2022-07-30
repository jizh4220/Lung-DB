import request from '@/utils/request'

export function login(data) {
  return request({
    url: "http://127.0.0.1:5000/api/user/login", //flask backend url
    method: 'post', //method
    data //username, password
  })
}
