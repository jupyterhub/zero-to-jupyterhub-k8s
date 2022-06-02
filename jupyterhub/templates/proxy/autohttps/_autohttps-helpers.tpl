{{- define "jupyterhub.autohttps.serviceAccountName" -}}
{{- if .Values.proxy.traefik.serviceAccount.create -}}
    {{ default (include "jupyterhub.autohttps.fullname" .) .Values.proxy.traefik.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.proxy.traefik.serviceAccount.name }}
{{- end -}}
{{- end -}}
