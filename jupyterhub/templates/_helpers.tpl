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
TODO: Set the name field using a helper
- Optionally add release name and such to it using some setting in .Values.
- Allow appending stuff for specific objects we already do this.
*/}}


{{- /*
Sets label: app.
*/}}
{{- define "jupyterhub.name" -}}
{{- .appLabel | default .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}


{{- /*
Sets labels: component, app, chart, release, heritage.
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
Sets selection labels: component, app, release.
*/}}
{{- define "jupyterhub.matchLabels" }}
{{- $_ := merge (dict "matchLabels" true) . }}
{{- include "jupyterhub.labels" $_ }}
{{- end }}
