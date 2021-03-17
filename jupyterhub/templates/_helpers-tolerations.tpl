{{- define "jupyterhub.tolerations" }}
{{- /*
This function expects a dictionary with two keys:
"root" (top level .) and "extraTolerations" (.Values.<thing>.tolerations)

Use in yaml files:
{{- with include "jupyterhub.tolerations" (dict "root" . "extraTolerations" .Values.prePuller.hook.tolerations) }}
      tolerations:
        {{- . | indent 8 }}
{{- end }}

Note in example if this returns nil (no defaultTolerations or extraTolerations) 
then the `tolerations` line is not rendered in the yaml file
*/}}
{{- if .root.Values.defaultTolerations.enabled }}
{{- with .root.Values.defaultTolerations.tolerations }}
{{- . | toYaml | nindent 0 }}
{{- end }}
{{- end }}
{{- if .extraTolerations }}
{{- with .extraTolerations }}
{{- . | toYaml | nindent 0 }}
{{- end }}
{{- end }}
{{- end }}

