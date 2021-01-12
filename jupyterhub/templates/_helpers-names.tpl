{{- /*

There are five modes to name resources, for more details see schema.yaml or the
rendered configuration reference under fullnameOverride / nameOverride.

    1. namespaced:   component                          fullnameOverride: "",   nameOverride: ?
       cluster wide: release-component
    2. independent:  fullnameOverride-component         fullnameOverride: str,  nameOverride: ?
    3. independent:  release-component                  fullnameOverride: null, nameOverride: ""
    4. independent:  release-(nameOverride-)component   fullnameOverride: null, nameOverride: str   (omitted if contained in release)
    5. independent:  release-(chart-)component          fullnameOverride: null, nameOverride: null  (omitted if contained in release)

With such dynamic naming, referencing them is a bit complicated. With dynamic
names, we cannot use hardcoded strings. So, how do we reference them from this
chart and parent charts depending on this chart?

From templates...

    Rely on the named templates below, so instead of referencing "hub" as a name,
    reference the named template "jupyterhub.hub.fullname" passing the . scope.

From containers...

    Rely on the hub ConfigMap which both has a blob of YAML and individual
    key/value pairs.

*/}}

{{- /* The chart's resources' name prefix */}}
{{- define "jupyterhub.fullname" -}}
    {{- /*
        A hack to avoid issues from invoking this from a parent Helm chart.

        Caveats and notes:
            1. While parent charts can, their parents chart can't reference these
            2. The parent chart must not use an alias for this chart
            3. There is no failsafe workaround to above due to
            https://github.com/helm/helm/issues/9214.
            4. Note that .Chart is of type *chart.Metadata needs to be casted to a
            normal dict by doing "toYaml | fromYaml" for normal dict inspection.
    */}}
    {{- $fullname_override := .Values.fullnameOverride }}
    {{- $name_override := .Values.nameOverride }}
    {{- if ne .Chart.Name "jupyterhub" }}
        {{- $fullname_override = .Values.jupyterhub.fullnameOverride }}
        {{- $name_override = .Values.jupyterhub.nameOverride }}
    {{- end }}

    {{- if eq (typeOf $fullname_override) "string" }}
        {{- $fullname_override }}
    {{- else }}
        {{- $name := $name_override | default .Chart.Name }}
        {{- if contains $name .Release.Name }}
            {{- .Release.Name }}
        {{- else }}
            {{- .Release.Name }}-{{ $name }}
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
    {{- /* A hack to avoid issues from invoking this from a parent Helm chart. */}}
    {{- $existing_secret := .Values.hub.existingSecret }}
    {{- if ne .Chart.Name "jupyterhub" }}
        {{- $existing_secret = .Values.jupyterhub.hub.existingSecret }}
    {{- end }}
    {{- if $existing_secret }}
        {{- $existing_secret }}
    {{- else }}
        {{- include "jupyterhub.hub.fullname" . }}
    {{- end }}
{{- end }}

{{- /* hub PVC */}}
{{- define "jupyterhub.hub-pvc.fullname" -}}
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
{{- define "jupyterhub.user-scheduler-deploy.fullname" -}}
    {{- include "jupyterhub.fullname.dash" . }}user-scheduler
{{- end }}

{{- /* user-scheduler leader election lock resource */}}
{{- define "jupyterhub.user-scheduler-lock.fullname" -}}
    {{- include "jupyterhub.user-scheduler-deploy.fullname" . }}-lock
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


{{- /*
    Cluster wide resources
*/}}

{{- /* Priority */}}
{{- define "jupyterhub.priority.fullname" -}}
    {{- if (include "jupyterhub.fullname.dash" .) }}
        {{- include "jupyterhub.fullname.dash" . }}
    {{- else }}
        {{- .Release.Name }}-default-priority
    {{- end }}
{{- end }}

{{- /* user-placeholder Priority */}}
{{- define "jupyterhub.user-placeholder-priority.fullname" -}}
    {{- if (include "jupyterhub.fullname.dash" .) }}
        {{- include "jupyterhub.user-placeholder.fullname" . }}
    {{- else }}
        {{- .Release.Name }}-user-placeholder-priority
    {{- end }}
{{- end }}

{{- /* user-scheduler ref - a cluster wide reference */}}
{{- define "jupyterhub.user-scheduler.fullname" -}}
    {{- if (include "jupyterhub.fullname.dash" .) }}
        {{- include "jupyterhub.user-scheduler-deploy.fullname" . }}
    {{- else }}
        {{- .Release.Name }}-user-scheduler
    {{- end }}
{{- end }}

{{- /*
    name-templates - a template rendering all name templates so its easy to
    emit them to a configmap.

    IMPORTANT: Ensure 1:1 mapping of references
*/}}
{{- define "jupyterhub.name-templates" -}}
fullname: {{ include "jupyterhub.fullname" . | quote }}
hub: {{ include "jupyterhub.hub.fullname" . | quote }}
hub-secret: {{ include "jupyterhub.hub-secret.fullname" . | quote }}
hub-pvc: {{ include "jupyterhub.hub-pvc.fullname" . | quote }}
proxy: {{ include "jupyterhub.proxy.fullname" . | quote }}
proxy-api: {{ include "jupyterhub.proxy-api.fullname" . | quote }}
proxy-http: {{ include "jupyterhub.proxy-http.fullname" . | quote }}
proxy-public: {{ include "jupyterhub.proxy-public.fullname" . | quote }}
proxy-public-tls: {{ include "jupyterhub.proxy-public-tls.fullname" . | quote }}
proxy-public-manual-tls: {{ include "jupyterhub.proxy-public-manual-tls.fullname" . | quote }}
autohttps: {{ include "jupyterhub.autohttps.fullname" . | quote }}
user-scheduler-deploy: {{ include "jupyterhub.user-scheduler-deploy.fullname" . | quote }}
user-scheduler-lock: {{ include "jupyterhub.user-scheduler-lock.fullname" . | quote }}
user-placeholder: {{ include "jupyterhub.user-placeholder.fullname" . | quote }}
hook-image-awaiter: {{ include "jupyterhub.hook-image-awaiter.fullname" . | quote }}
hook-image-puller: {{ include "jupyterhub.hook-image-puller.fullname" . | quote }}
continuous-image-puller: {{ include "jupyterhub.continuous-image-puller.fullname" . | quote }}
singleuser: {{ include "jupyterhub.singleuser.fullname" . | quote }}
image-pull-secret: {{ include "jupyterhub.image-pull-secret.fullname" . | quote }}
ingress: {{ include "jupyterhub.ingress.fullname" . | quote }}
priority: {{ include "jupyterhub.priority.fullname" . | quote }}
user-placeholder-priority: {{ include "jupyterhub.user-placeholder-priority.fullname" . | quote }}
user-scheduler: {{ include "jupyterhub.user-scheduler.fullname" . | quote }}
{{- end }}
