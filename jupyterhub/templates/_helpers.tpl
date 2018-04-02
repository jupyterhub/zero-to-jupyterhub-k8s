{{/*
Generates labels based on 
- component: the template parent folder's name / the template's filename
  - looks for componentPrefix / componentSuffix
- app: 
  - looks for appLabel
*/}}
{{- define "jupyterhub.labels" -}}
{{- $componentFallback := .Template.Name | base | trimSuffix ".yaml" -}}
{{- $component := .Template.Name | dir | base | trimPrefix "templates" -}}
{{- $component := default $componentFallback $component -}}
{{- $component := print (default "" .componentPrefix) $component (default "" .componentSuffix) -}}
component: {{ $component }}
app: {{ include "jupyterhub.name" . }}
chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
release: {{ .Release.Name }}
heritage: {{ .Release.Service }}
{{- end -}}

{{/*
A slimmed jupyterhub.labels template
*/}}
{{- define "jupyterhub.matchLabels" -}}
{{- $componentFallback := .Template.Name | base | trimSuffix ".yaml" -}}
{{- $component := .Template.Name | dir | base | trimPrefix "templates" -}}
{{- $component := default $componentFallback $component -}}
{{- $component := print (default "" .componentPrefix) $component (default "" .componentSuffix) -}}
app: {{ include "jupyterhub.name" . }}
component: {{ $component }}
release: {{ .Release.Name }}
{{- end -}}

{{/*
Generates a value for the app label.
*/}}
{{- define "jupyterhub.name" -}}
{{- default .Chart.Name .appLabel | trunc 63 | trimSuffix "-" -}}
{{- end -}}