{{- define "jupyterhub.defaultTolerations" -}}
{{- if .Values.hub.defaultTolerations.enabled }}
- key: hub.jupyter.org_dedicated
  operator: Equal
  value: user
  effect: NoSchedule
- key: hub.jupyter.org/dedicated
  operator: Equal
  value: user
  effect: NoSchedule
{{- end }}
{{- end }}
