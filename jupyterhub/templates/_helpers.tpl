{{- /*
- component:
  - A: .componentLabel
  - B: The template parent folder's name
  - C: The template's filename if living in the root folder
  - Extra: Also augments componentPrefix componentSuffix
- app: 
  - A: .appLabel
  - B: .Chart.Name
*/}}


{{- /*
Sets the app label.
*/}}
{{- define "jupyterhub.name" -}}
{{- .appLabel | default .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}


{{- /*
Sets the Helm's recommend labels: component, app, chart, release, heritage.
*/}}
{{- define "jupyterhub.labels" }}
{{- $file := .Template.Name | base | trimSuffix ".yaml" }}
{{- $parent := .Template.Name | dir | base | trimPrefix "templates" }}
{{- $component := .componentLabel | default $parent | default $file }}
{{- $component := print (.componentPrefix | default "") $component (.componentSuffix | default "") -}}
component: {{ $component }}
app: {{ include "jupyterhub.name" . }}
{{- if not .matchLabels }}
chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end }}
release: {{ .Release.Name }}
{{- if not .matchLabels }}
heritage: {{ .Release.Service }}
{{- end }}
{{- end }}

{{- /*
Sets labels to select another object with: component, app, release.
*/}}
{{- /*
A slimmed version of jupyterhub.labels template for selection
*/}}
{{- define "jupyterhub.matchLabels" }}
{{- $_ := merge (dict "matchLabels" true) . -}}
{{- include "jupyterhub.labels" $_ }}
{{- end }}