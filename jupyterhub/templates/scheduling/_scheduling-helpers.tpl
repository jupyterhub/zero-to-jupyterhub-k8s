{{- /*
  jupyterhub.prepareScope
    Requires the .podKind field.

    prepareScope sets fields on the scope to be used by the
    jupyterhub.tolerations and jupyterhub.affinity helm template functions
    below.
*/}}
{{- define "jupyterhub.prepareScope" -}}
{{- /* Update the copied scope */}}
{{- $dummy := set . "component" (include "jupyterhub.componentLabel" .) }}

{{- /* Fetch relevant information */}}
{{- $dummy := set . "tolerationsList" (include "jupyterhub.tolerationsList" .) }}
{{- $dummy := set . "tolerations" (include "jupyterhub.tolerations" .) }}
{{- $dummy := set . "hasTolerations" .tolerations }}
{{- end }}



{{- /*
  jupyterhub.tolerations
    Refactors the setting of the user pods tolerations field.
*/}}
{{- define "jupyterhub.tolerations" -}}
{{- if .tolerationsList -}}
tolerations:
  {{- .tolerationsList | nindent 2 }}
{{- end }}
{{- end }}

{{- define "jupyterhub.tolerationsList" -}}
{{- if eq .podKind "core" -}}
{{- else if eq .podKind "user" -}}
- key: hub.jupyter.org_dedicated
  operator: Equal
  value: user
  effect: NoSchedule
- key: hub.jupyter.org/dedicated
  operator: Equal
  value: user
  effect: NoSchedule
{{- if .Values.singleuser.extraTolerations -}}
{{- .Values.singleuser.extraTolerations | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}
{{- end }}
