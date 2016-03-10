#! /usr/bin/env python
# coding:utf-8
from fabric.api import run, sudo, env
from fabric.api import settings, cd, task, roles, execute
from fabric.colors import green
"""
    功能： 管理pyspider的各个组件的启动
"""

env.user = 'forker'
env.password = 'forkerLinux'
env.roledefs = {
    'result_worker': [],
    'fetcher': ['192.168.12.58'],
    'processor': [],
    'scheduler': [],
    'webui': ['192.168.12.58'],
    'public': []
}
env.conf_file = '/home/app/jd_spider/supervisor.conf'

@roles('result_worker')
def result_worker_task(param='start'):
    result = sudo('supervisorctl %s result_worker:' % param)
    print(green('result_worker %s success.' % param))


@roles('fetcher')
def fetcher_task(param='start'):
    sudo('supervisorctl %s fetcher:' % param)
    print(green('fetcher %s success.' % param))


@roles('processor')
def processor_task(param='start'):
    sudo('supervisorctl %s processor:' % param)
    print(green('processor %s success.' % param))


@roles('scheduler')
def scheduler_task(param='start'):
    sudo('supervisorctl %s scheduler:' % param)
    print(green('scheduler %s success.' % param))


@roles('public')
def create_link():
    print(green('create conf file link...'))
    sudo('ln -s %s /etc/supervisor/conf.d/jd_spider.conf' % env.conf_file)
    print(green('create file link finish.'))


@roles('webui')
def webui_task(param='start'):
    sudo('supervisorctl %s webui' % param)
    print(green('webui %s success.' % param))

@task
def go():
    # 创建文件链接
    execute(create_link)

    task_dict = {
        'result_worker': result_worker_task,
        'fetcher': fetcher_task,
        'processor': processor_task,
        'scheduler': scheduler_task,
        'webui': webui_task
    }
    for role in env.roledefs:
        if len(env.roledefs[role]) > 0:
            execute(task_dict[role], param='start')
