{{- /*
  This file contains helpers to systematically name, label and create
  matchLabels for the Kubernetes objects we define in the .yaml template files.

  Typical usage within a Kubernetes object:

  ```yaml
    labels:
      {{- include "jupyterhub.labels" . | nindent 4 }}
  ```

  To control the helpers' behavior, augment the scope passed to the helper by
  merging it with additional key/value pairs like below. In this case the
  `component` label had to be set explicitly instead of implicitly from the
  .yaml files location.

  ```yaml
  podSelector:
    matchLabels:
      {{- $_ := merge (dict "componentLabel" "singleuser-server") . }}
      {{- include "jupyterhub.matchLabels" $_ | nindent 6 }}
  ```
*/}}


{{- /*
  jupyterhub.name:
    Used to provide the app label's value and within the jupyterhub.fullname
    helper.

  NOTE: It will return the provided scope's .appLabel or default to the chart's
        name.

  TODO:
  - [ ] Support overriding this value with some setting in .Values as is common
        within kubernetes/charts projects
*/}}
{{- define "jupyterhub.name" }}
{{- .appLabel | default .Chart.Name }}
{{- end }}


{{- /*
  jupyterhub.fullname:
    Used to populate the name field value.
    NOTE: some name fields are limited to 63 characters by the DNS naming spec.

  TODO:
  - [ ] Start setting the name fields using this helper.
  - [ ] Update the helper to allow appending the name, as a conflict will
        arise if multiple objects of the same type is defined in the same
        template folder.
  - [ ] Optionally prefix the release name based on some setting in .Values to
        allow for multiple deployments within a single namespace.
*/}}
{{- define "jupyterhub.fullname" }}
{{- $name := include "jupyterhub.name" . }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}


{{- /*
  jupyterhub.labels:
    Used to provide the labels: component, app, release, (chart and heritage).

  NOTE: The component label is determined by either...
        - 1: The provided scope's .componentLabel 
        - 2: The template's filename if living in the root folder
        - 3: The template parent folder's name
        ... and is combined with .componentPrefix and .componentSuffix
*/}}
{{- define "jupyterhub.labels" }}
{{- $file := .Template.Name | base | trimSuffix ".yaml" }}
{{- $parent := .Template.Name | dir | base | trimPrefix "templates" }}
{{- $component := .componentLabel | default $parent | default $file }}
{{- $component := print (.componentPrefix | default "") $component (.componentSuffix | default "") -}}
component: {{ $component }}
app: {{ include "jupyterhub.name" . }}
release: {{ .Release.Name }}
{{- if not .matchLabels }}
chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
heritage: {{ .Release.Service }}
{{- end }}
{{- end }}


{{- /*
  jupyterhub.matchLabels:
    Used to provide pod selection labels: component, app, release.
*/}}
{{- define "jupyterhub.matchLabels" }}
{{- $_ := merge (dict "matchLabels" true) . }}
{{- include "jupyterhub.labels" $_ }}
{{- end }}


{{- /*
  jupyterhub.podCullerSelector:
    Used to by the pod culler to select singleuser-server pods.
*/}}
{{- define "jupyterhub.podCullerSelector" }}
"component={{ $component }},app={{ include "jupyterhub.name" . }},release={{ .Release.Name }}"
{{- end }}
