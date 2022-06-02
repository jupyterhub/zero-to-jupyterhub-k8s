{{- define "jupyterhub.hub.ServiceAccountName" -}}
{{- if .Values.hub.serviceAccount.create -}}
    {{ default (include "jupyterhub.hub.fullname" .) .Values.hub.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.hub.serviceAccount.name }}
{{- end -}}
{{- end -}}
