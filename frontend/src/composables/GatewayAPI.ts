import { useHttp } from '@/plugins/http'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'
import { useRuntimeStore } from '@/stores/runtime'
import type { AxiosResponse } from 'axios'

interface loginIdents {
  user: string
  password: string
}

export interface ClusterPermissions {
  name: string
  roles: string[]
  actions: string[]
}

interface GatewayLoginResponse {
  token: string
  fullname: string
  groups: string[]
  clusters: ClusterPermissions[]
}

export class ClusterStats {
  resources: {
    nodes: number
    cores: number
  }
  jobs: {
    running: number
    total: number
  }
  constructor() {
    this.resources = { nodes: 0, cores: 0 }
    this.jobs = { running: 0, total: 0 }
  }
}

export interface ClusterJob {
  id: number
  job_id: number
  user_name: string
  account: string
  job_state: string
  partition: string
}

export interface ClusterNode {
  id: number
  name: string
  cpus: number
  cores: number
  real_memory: number
  state: Array<string>
  partitions: Array<string>
}

export interface ClusterQos {
  name: string
  description: string
}

export class AuthenticationError extends Error {
  constructor(message: string) {
    super(message)
  }
}

class APIServerError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

class RequestError extends Error {
  constructor(message: string) {
    super(message)
  }
}

export function useGatewayAPI() {
  const http = useHttp()
  const authStore = useAuthStore()
  const runtimeStore = useRuntimeStore()

  async function requestServer(func: Function): Promise<AxiosResponse> {
    try {
      return await func()
    } catch (error: any) {
      if (error.response) {
        /* Server replied with error status code */
        throw new APIServerError(error.response.status, error.response.data.description)
      } else if (error.request) {
        /* No reply from server */
        throw new RequestError(`Request error: ${error.message}`)
      } else {
        /* Something else happening when setting up the request */
        throw new RequestError(`Setting up request error: ${error.message}`)
      }
    }
  }

  async function getWithToken(resource: string): Promise<any> {
    console.log(`Slurm-web gateway API get with token ${resource}`)
    const config = {
      headers: { Authorization: `Bearer ${authStore.token}` }
    }
    return (
      await requestServer(() => {
        return http.get(resource, config)
      })
    ).data
  }

  async function post(resource: string, data: any): Promise<any> {
    console.log(`Slurm-web gateway API post ${resource}`)
    return (
      await requestServer(() => {
        return http.post(resource, data)
      })
    ).data
  }

  async function login(idents: loginIdents): Promise<GatewayLoginResponse> {
    try {
      return (await post('/login', idents)) as GatewayLoginResponse
    } catch (error: any) {
      /* Translate 401 APIServerError into AuthenticationError */
      if (error instanceof APIServerError && error.status == 401) {
        throw new AuthenticationError(error.message)
      }
      throw error
    }
  }

  async function stats(cluster: string): Promise<ClusterStats> {
    try {
      return (await getWithToken(`/agents/${cluster}/stats`)) as ClusterStats
    } catch (error: any) {
      /* Translate 401 APIServerError into AuthenticationError */
      if (error instanceof APIServerError && error.status == 401) {
        throw new AuthenticationError(error.message)
      }
      throw error
    }
  }

  async function jobs(cluster: string): Promise<ClusterJob[]> {
    try {
      return (await getWithToken(`/agents/${cluster}/jobs`)) as ClusterJob[]
    } catch (error: any) {
      /* Translate 401 APIServerError into AuthenticationError */
      if (error instanceof APIServerError && error.status == 401) {
        throw new AuthenticationError(error.message)
      }
      throw error
    }
  }

  async function nodes(cluster: string): Promise<ClusterNode[]> {
    try {
      return (await getWithToken(`/agents/${cluster}/nodes`)) as ClusterNode[]
    } catch (error: any) {
      /* Translate 401 APIServerError into AuthenticationError */
      if (error instanceof APIServerError && error.status == 401) {
        throw new AuthenticationError(error.message)
      }
      throw error
    }
  }

  async function qos(cluster: string): Promise<ClusterQos[]> {
    try {
      return (await getWithToken(`/agents/${cluster}/qos`)) as ClusterQos[]
    } catch (error: any) {
      /* Translate 401 APIServerError into AuthenticationError */
      if (error instanceof APIServerError && error.status == 401) {
        throw new AuthenticationError(error.message)
      }
      throw error
    }
  }

  return { login, stats, jobs, nodes, qos }
}
