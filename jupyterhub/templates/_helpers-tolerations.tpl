{{- /*
  jupyterhub.coreTolerations

    Lists the tolerations for node taints that the core pods should have.

    This function expects a dictionary of two keys:

      - "root",             should be .
      - "extraTolerations", should be .Values.<thing>.tolerations

    Example:

      {{- with include "jupyterhub.coreTolerations" (dict "root" . "extraTolerations" .Values.hub.tolerations) }}
      tolerations:
        {{- . | nindent 8 }}
      {{- end }}
*/}}
{{- define "jupyterhub.coreTolerations" }}
{{- with concat .root.Values.scheduling.corePods.tolerations (.extraTolerations | default list) }}
{{- . | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}

{{- /*
  jupyterhub.userTolerations

    Lists the tolerations for node taints that the user pods should have.

    This function expects a dictionary of two keys:

      - "root",             should be .
      - "extraTolerations", should be .Values.<thing>.tolerations

    Example:

      {{- with include "jupyterhub.userTolerations" (dict "root" . "extraTolerations" .Values.prePuller.extraTolerations) }}
      tolerations:
        {{- . | nindent 8 }}
      {{- end }}
*/}}
{{- define "jupyterhub.userTolerations" }}
{{- with concat .root.Values.scheduling.userPods.tolerations .root.Values.singleuser.extraTolerations (.extraTolerations | default list) }}
{{- . | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}
