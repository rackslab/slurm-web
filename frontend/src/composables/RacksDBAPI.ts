import type { AxiosInstance } from 'axios'

export type RacksDBAPIImage = ImageBitmapSource
export type RacksDBAPIResult = RacksDBAPIImage

export function useRacksDBAPI(http: AxiosInstance) {
  async function racksDBGet(resource: string): Promise<ArrayBuffer> {
    console.log(`RacksDB get ${resource}`)
    try {
      const response = await http.get(resource, {
        responseType: 'arraybuffer'
      })
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

  async function infrastructureImagePng(infrastructure: string): Promise<RacksDBAPIImage> {
    return new Blob([
      await racksDBGet(`/api/racksdb/draw/infrastructure/${infrastructure}.png`)
    ]) as RacksDBAPIImage
  }

  return { infrastructureImagePng }
}
