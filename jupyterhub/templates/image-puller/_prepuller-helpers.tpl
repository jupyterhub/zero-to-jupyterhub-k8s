{{- define "jupyterhub.hook-image-awaiter.serviceAccountName" -}}
{{- if .Values.prePuller.hook.serviceAccount.create -}}
    {{ default (include "jupyterhub.hook-image-awaiter.fullname" .) .Values.prePuller.hook.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.prePuller.hook.serviceAccount.name }}
{{- end -}}
{{- end -}}
