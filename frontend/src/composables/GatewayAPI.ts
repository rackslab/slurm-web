import { useHttp } from '@/plugins/http'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'
import { useRuntimeStore } from '@/stores/runtime'
import type { AxiosResponse } from 'axios'

interface loginIdents {
  user: string
  password: string
}

export interface ClusterDescription {
  name: string
  permissions: ClusterPermissions
  stats?: ClusterStats
}

interface ClusterPermissions {
  roles: string[]
  actions: string[]
}

export interface UserDescription {
  login: string
  fullname: string
}

interface GatewayLoginResponse extends UserDescription {
  token: string
  groups: string[]
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
  job_id: number
  user_name: string
  account: string
  job_state: string
  partition: string
}

export interface ClusterNode {
  name: string
  cores: number
  cpus: number
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

export class PermissionError extends Error {
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
  let controller = new AbortController()

  async function requestServer(func: Function): Promise<AxiosResponse> {
    try {
      return await func()
    } catch (error: any) {
      if (error.response) {
        /* Server replied with error status code */
        if (error.response.status == 401) {
          throw new AuthenticationError(error.message)
        } else if (error.response.status == 403) {
          throw new PermissionError(error.message)
        } else {
          throw new APIServerError(error.response.status, error.response.data.description)
        }
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
      headers: { Authorization: `Bearer ${authStore.token}` },
      signal: controller.signal
    }
    return (
      await requestServer(() => {
        return http.get(resource, config)
      })
    ).data
  }

  async function post(resource: string, data: any): Promise<any> {
    console.log(`Slurm-web gateway API post ${resource}`)
    const config = {
      signal: controller.signal
    }
    return (
      await requestServer(() => {
        return http.post(resource, data, config)
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

  async function clusters(): Promise<Array<ClusterDescription>> {
    return (await getWithToken(`/clusters`)) as ClusterDescription[]
  }

  async function users(): Promise<Array<UserDescription>> {
    return (await getWithToken(`/users`)) as UserDescription[]
  }

  async function stats(cluster: string): Promise<ClusterStats> {
    return (await getWithToken(`/agents/${cluster}/stats`)) as ClusterStats
  }

  async function jobs(cluster: string): Promise<ClusterJob[]> {
    return (await getWithToken(`/agents/${cluster}/jobs`)) as ClusterJob[]
  }

  async function nodes(cluster: string): Promise<ClusterNode[]> {
    return (await getWithToken(`/agents/${cluster}/nodes`)) as ClusterNode[]
  }

  async function qos(cluster: string): Promise<ClusterQos[]> {
    return (await getWithToken(`/agents/${cluster}/qos`)) as ClusterQos[]
  }

  function abort() {
    /* Abort all pending requests */
    controller.abort()
    controller = new AbortController()
  }

  return { login, clusters, users, stats, jobs, nodes, qos, abort }
}
