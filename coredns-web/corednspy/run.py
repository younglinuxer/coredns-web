#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, render_template, request, flash,redirect,url_for
import etcd3
import json,re

etcd = etcd3.client(host='etcd-dns', port='2379')

def get_dns():
    data = etcd.get_all_response()
    k_dict = []
    for i in data.kvs:
        if (str(i.key).split('/')[0]) == '' and (str(i.key).split('/')[1] == 'coredns'):
            domain = i.key.split('/')
            domain.reverse()
            del domain[-2:]
            result = {'domain': '.'.join(str(i) for i in domain), 'ip': json.loads(i.value)['host']}
            k_dict.append(result)
    return k_dict


def add_dns(domain='www.example.com', host='127.0.0.1'):
    key = domain.split('.')
    key.append('coredns')
    key.reverse()
    value = '{"host":"%s","ttl":10}' % host
    d_key = '/' + "/".join(str(i) for i in key)
    print d_key, value
    etcd.put(d_key, value)


app = Flask(__name__)
app.secret_key = 'kjsensldfneapk'


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        domain = request.form['domain']
        ip_value = request.form['ip_value']
        dnstype = request.form['dnstype']
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if domain == "manager" or domain == "enterprise" or domain == "personal" or domain == "evaluation" or domain == "www" or domain == "":
            flash(u'过滤敏感信息')
            return render_template('index.html')
        elif not compile_ip.match(ip_value):
            print 'IP地址不合法'
            flash(u'IP地址不合法')
            return render_template('index.html')
        c = add_dns(domain=domain,host=ip_value)
        print c
        flash(u'更新域名完成请稍后查看')
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('index.html', jxjl=get_dns())
    return render_template('index.html')

#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081,debug=True)


