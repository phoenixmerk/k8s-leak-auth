# k8s-leak-auth
《暴露 Kubernetes 秘密的滴答作响的供应链攻击炸弹》参考了Aqua的文章写的一个简单的本地检测脚本 The Ticking Supply Chain Attack Bomb of Exposed Kubernetes Secrets

## dockerLocal.py
docker版本低于18.09将会在本地~/.docker或者~/.dockercfg存储相关的存储库auth信息，脚本将检查这两个目录是否存在
## kubernetes.py
kubernetes将两个文件存储为secrets，脚本将检查这两项并输出secrets
kubernetes.io/dockercfg
kubernetes.io/dockerconfig
