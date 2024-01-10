/*
 SPDX-License-Identifier: Apache-2.0
*/
import exception from './zh-CN/exception';
import globalHeader from './zh-CN/globalHeader';
import login from './zh-CN/login';
import menu from './zh-CN/menu';
import pwa from './zh-CN/pwa';
import component from './zh-CN/component';
import Organization from './zh-CN/Organization';
import operatorUser from './zh-CN/operatorUser';
import form from './zh-CN/form';
import Agent from './zh-CN/Agent';
import Node from './zh-CN/Node';
import fabricCa from './zh-CN/fabric/ca';
import Network from './zh-CN/Network';
import Channel from './zh-CN/Channel';
import ChainCode from './zh-CN/Chaincode';

export default {
  'navBar.lang': '语言',
  'layout.user.link.help': '帮助',
  'layout.user.link.privacy': '隐私',
  'layout.user.link.terms': '条款',
  'app.home.introduce': '介绍',
  'app.forms.basic.title': '基础表单',
  'app.forms.basic.description':
    '表单页用于向用户收集或验证信息，基础表单常见于数据项较少的表单场景。',
  ...exception,
  ...globalHeader,
  ...login,
  ...menu,
  ...pwa,
  ...component,
  ...Organization,
  ...Agent,
  ...operatorUser,
  ...form,
  ...Node,
  ...fabricCa,
  ...Network,
  ...Channel,
  ...ChainCode,
};
