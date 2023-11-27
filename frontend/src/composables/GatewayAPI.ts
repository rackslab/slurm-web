import type { AxiosInstance } from 'axios'

export type RacksDBAPIImage = ImageBitmapSource
export type RacksDBAPIResult = RacksDBAPIImage

interface loginIdents {
  user: string
  password: string
}

interface GatewayLoginResponse {
  token: string
  clusters: string[]
}

export function useGatewayAPI(http: AxiosInstance) {
  async function get(resource: string): Promise<any> {
    console.log(`Slurm-web gateway API get ${resource}`)
    try {
      let response = await http.get(resource)
      return response.data
    } catch (error: any) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      if (error.response) {
        console.log('errors: ' + error.response.status + ' ' + error.response.data.error)
      } else if (error.request) {
        // The request was made but no response was received `error.request` is
        // an instance of XMLHttpRequest in the browser.
        console.log(error.request)
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message)
      }
      console.log(error.config)
      throw error
    }
  }

  async function post(resource: string, data: any): Promise<any> {
    console.log(`Slurm-web gateway API post ${resource}`)
    return (await http.post(resource, data)).data
  }

  async function login(idents: loginIdents): Promise<GatewayLoginResponse> {
    return (await post('/login', idents)) as GatewayLoginResponse
  }

  return { login }
}
