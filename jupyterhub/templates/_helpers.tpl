{{- /*
  ## About
  This file contains helpers to systematically name, label and select Kubernetes
  objects we define in the .yaml template files.


  ## Declared helpers
  - appLabel          |
  - componentLabel    |
  - nameField         | uses componentLabel
  - commonLabels      | uses appLabel
  - labels            | uses commonLabels
  - matchLabels       | uses labels
  - podCullerSelector | uses matchLabels


  ## Example usage
  ```yaml
  # Excerpt from proxy/autohttps/deployment.yaml
  apiVersion: apps/v1beta2
  kind: Deployment
  metadata:
    name: {{ include "jupyterhub.nameField" . }}
    labels:
      {{- include "jupyterhub.labels" . | nindent 4 }}
  spec:
    selector:
      matchLabels:
        {{- $_ := merge (dict "appLabel" "kube-lego") . }}
        {{- include "jupyterhub.matchLabels" $_ | nindent 6 }}
    template:
      metadata:
        labels:
          {{- include "jupyterhub.labels" $_ | nindent 8 }}
          hub.jupyter.org/network-access-proxy-http: "true"
  ```

  NOTE:
    The "jupyterhub.matchLabels" and "jupyterhub.labels" is passed an augmented
    scope that will influence the helpers' behavior. It get the current scope
    "." but merged with a dictionary containing extra key/value pairs. In this
    case the "." scope was merged with a small dictionary containing only one
    key/value pair "appLabel: kube-lego". It is required for kube-lego to
    function properly. It is a way to override the default app label's value.
*/}}


{{- /*
  jupyterhub.appLabel:
    Used by "jupyterhub.labels".
*/}}
{{- define "jupyterhub.appLabel" -}}
{{ .Values.nameOverride | default .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}


{{- /*
  jupyterhub.componentLabel:
    Used by "jupyterhub.labels" and "jupyterhub.nameField".

    NOTE: The component label is determined by either...
    - 1: The provided scope's .componentLabel 
    - 2: The template's filename if living in the root folder
    - 3: The template parent folder's name
    -  : ...and is combined with .componentPrefix and .componentSuffix
*/}}
{{- define "jupyterhub.componentLabel" -}}
{{- $file := .Template.Name | base | trimSuffix ".yaml" -}}
{{- $parent := .Template.Name | dir | base | trimPrefix "templates" -}}
{{- $component := .componentLabel | default $parent | default $file -}}
{{- $component := print (.componentPrefix | default "") $component (.componentSuffix | default "") -}}
{{ $component }}
{{- end }}


{{- /*
  jupyterhub.nameField:
    Populates the name field's value.
    NOTE: some name fields are limited to 63 characters by the DNS naming spec.

  TODO:
  - [ ] Set all name fields using this helper.
  - [ ] Optionally prefix the release name based on some setting in
        .Values to allow for multiple deployments within a single namespace.
*/}}
{{- define "jupyterhub.nameField" -}}
{{- $name := print (.namePrefix | default "") (include "jupyterhub.componentLabel" .) (.nameSuffix | default "") -}}
{{ printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}


{{- /*
  jupyterhub.commonLabels:
    Foundation for "jupyterhub.labels".
    Provides labels: app, release, (chart and heritage).
*/}}
{{- define "jupyterhub.commonLabels" -}}
app: {{ .appLabel | default (include "jupyterhub.appLabel" .) }}
release: {{ .Release.Name }}
{{- if not .matchLabels }}
chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
heritage: {{ .heritageLabel | default .Release.Service }}
{{- end }}
{{- end }}


{{- /*
  jupyterhub.labels:
    Provides labels: component, app, release, (chart and heritage).
*/}}
{{- define "jupyterhub.labels" -}}
component: {{ include "jupyterhub.componentLabel" . }}
{{ include "jupyterhub.commonLabels" . }}
{{- end }}


{{- /*
  jupyterhub.matchLabels:
    Used to provide pod selection labels: component, app, release.
*/}}
{{- define "jupyterhub.matchLabels" -}}
{{- $_ := merge (dict "matchLabels" true) . -}}
{{ include "jupyterhub.labels" $_ }}
{{- end }}


{{- /*
  jupyterhub.podCullerSelector:
    Used to by the pod-culler to select singleuser-server pods. 
    It simply reformats "jupyterhub.matchLabels".
*/}}
{{- define "jupyterhub.podCullerSelector" -}}
{{ include "jupyterhub.matchLabels" . | replace ": " "=" | replace "\n" "," | quote }}
{{- end }}
