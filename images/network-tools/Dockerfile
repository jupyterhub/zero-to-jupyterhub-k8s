# FIXME: use of alpine:3.19 makes iptables work in "nf_tables" mode instead of
#        "legacy" mode, and then our init container breaks.
#
#        ref: https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/3368
#
FROM alpine:3.18

# VULN_SCAN_TIME=2024-01-29_05:13:22

RUN apk add --no-cache iptables
