import { stringify } from 'qs';
import request from '@/utils/request';

export async function listChannel(params) {
  return request(`/api/v1/channels?${stringify(params)}`);
}

export async function createChannel(params) {
  return request('/api/v1/channels', {
    method: 'POST',
    data: params,
  });
}

export async function getChannel(id) {
  return request(`/api/v1/channels/${id}`);
}

export async function getNodeConfig(params) {
  return request(`/api/v1/channels/${params.id}/configs`, {
    method: 'GET',
    responseType: 'json',
    getResponse: true,
  });
}

export async function updateChannelConfig(id, params) {
  return request(`/api/v1/channels/${id}`, {
    method: 'PUT',
    data: params,
  });
}
