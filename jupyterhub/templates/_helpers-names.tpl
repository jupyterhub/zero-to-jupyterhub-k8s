{{- /* FIXME:
This named template is introduced byt not yet activated to
serve a purpose until everything would work when using it.
*/}}
{{- /* The chart's resources' name prefix */}}
{{- define "jupyterhub.fullname" -}}
{{- if not "FORCEFULLY DISABLED" }}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride }}
{{- else }}
{{- .Release.Name }}
{{- end }}
{{- end }}
{{- end }}

{{- /* The chart's resources' name prefix with a separator dash */}}
{{- define "jupyterhub.fullname.dash" -}}
{{- if (include "jupyterhub.fullname" .) }}
{{- include "jupyterhub.fullname" . }}-
{{- end }}
{{- end }}



{{- /* hub Deployment */}}
{{- define "jupyterhub.hub.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}hub
{{- end }}

{{- /* hub-secret Secret */}}
{{- define "jupyterhub.hub-secret.fullname" -}}
{{- if .Values.hub.existingSecret }}
{{- .Values.hub.existingSecret }}
{{- else }}
{{- include "jupyterhub.hub.fullname" . }}-secret
{{- end }}
{{- end }}

{{- /* hub-db-dir PVC */}}
{{- define "jupyterhub.hub-db-dir.fullname" -}}
{{- include "jupyterhub.hub.fullname" . }}-db-dir
{{- end }}

{{- /* proxy Deployment */}}
{{- define "jupyterhub.proxy.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}proxy
{{- end }}

{{- /* proxy-api Service */}}
{{- define "jupyterhub.proxy-api.fullname" -}}
{{- include "jupyterhub.proxy.fullname" . }}-api
{{- end }}

{{- /* proxy-http Service */}}
{{- define "jupyterhub.proxy-http.fullname" -}}
{{- include "jupyterhub.proxy.fullname" . }}-http
{{- end }}

{{- /* proxy-public Service */}}
{{- define "jupyterhub.proxy-public.fullname" -}}
{{- include "jupyterhub.proxy.fullname" . }}-public
{{- end }}

{{- /* proxy-public-tls Secret */}}
{{- define "jupyterhub.proxy-public-tls.fullname" -}}
{{- include "jupyterhub.proxy-public.fullname" . }}-tls-acme
{{- end }}

{{- /* proxy-public-manual-tls Secret */}}
{{- define "jupyterhub.proxy-public-manual-tls.fullname" -}}
{{- include "jupyterhub.proxy-public.fullname" . }}-manual-tls
{{- end }}

{{- /* autohttps Deployment */}}
{{- define "jupyterhub.autohttps.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}autohttps
{{- end }}

{{- /* user-scheduler Deployment */}}
{{- define "jupyterhub.user-scheduler.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}user-scheduler
{{- end }}

{{- /* user-scheduler leader election lock resource */}}
{{- define "jupyterhub.user-scheduler-lock.fullname" -}}
{{- include "jupyterhub.user-scheduler.fullname" . }}-lock
{{- end }}

{{- /* user-placeholder StatefulSet */}}
{{- define "jupyterhub.user-placeholder.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}user-placeholder
{{- end }}

{{- /* image-awaiter Job */}}
{{- define "jupyterhub.hook-image-awaiter.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}hook-image-awaiter
{{- end }}

{{- /* hook-image-puller DaemonSet */}}
{{- define "jupyterhub.hook-image-puller.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}hook-image-puller
{{- end }}

{{- /* continuous-image-puller DaemonSet */}}
{{- define "jupyterhub.continuous-image-puller.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}continuous-image-puller
{{- end }}

{{- /* singleuser NetworkPolicy */}}
{{- define "jupyterhub.singleuser.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}singleuser
{{- end }}

{{- /* image-pull-secret Secret */}}
{{- define "jupyterhub.image-pull-secret.fullname" -}}
{{- include "jupyterhub.fullname.dash" . }}image-pull-secret
{{- end }}

{{- /* Ingress */}}
{{- define "jupyterhub.ingress.fullname" -}}
{{- if (include "jupyterhub.fullname.dash" .) }}
{{- include "jupyterhub.fullname.dash" . }}
{{- else -}}
jupyterhub
{{- end }}
{{- end }}
