import type { AxiosInstance } from 'axios'

export interface SlurmAPIResultMeta {
  Slurm: number
  plugin: number
}

export interface SlurmAPIResult {
  meta: SlurmAPIResultMeta
}

export interface SlurmAPINodesResult extends SlurmAPIResult {
  nodes: SlurmNode[]
}

export interface SlurmAPIJobsResult extends SlurmAPIResult {
  jobs: SlurmJob[]
}

export interface SlurmJob {
  id: number
  job_id: number
  user_name: string
  account: string
  job_state: string
  partition: string
}

export interface SlurmNode {
  id: number
  name: string
  cpus: number
  cores: number
  real_memory: number
  state: Array<string>
  partitions: Array<string>
}

export function useSlurmAPI(http: AxiosInstance, token: string | null) {
  async function slurmGet(resource: string): Promise<SlurmAPIResult> {
    if (token === null) {
      throw new Error('Unable to send HTTP GET request to Slurm API with null token')
    } else {
      console.log(`slurm get ${resource}`)
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      }
      try {
        const response = await http.get(resource, config)
        return response.data
      } catch (error: any) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        if (error.response) {
          console.log('errors: ' + error.response.status + ' ' + error.response.data.error)
        } else if (error.request) {
          // The request was made but no response was received `error.request` is an instance of XMLHttpRequest in the browser and an instance of
          // http.ClientRequest in node.js
          console.log(error.request)
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log('Error', error.message)
        }
        console.log(error.config)
        throw error
      }
    }
  }
  async function nodes(): Promise<Array<SlurmNode>> {
    const response = (await slurmGet('/api/slurm/v0.0.39/nodes')) as SlurmAPINodesResult
    return response.nodes
  }
  async function jobs(): Promise<Array<SlurmJob>> {
    const response = (await slurmGet('/api/slurm/v0.0.39/jobs')) as SlurmAPIJobsResult
    return response.jobs
  }

  return { slurmGet, nodes, jobs }
}
