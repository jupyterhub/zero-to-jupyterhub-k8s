{{- define "jupyterhub.defaultTolerations" -}}
{{- if .Values.defaultTolerations.enabled -}}
{{- with .Values.defaultTolerations.tolerations -}}
{{- . | toYaml | trimSuffix "\n" | nindent 0 -}}
{{- end -}}
{{- else -}}
{}
{{- end -}}
{{- end -}}
