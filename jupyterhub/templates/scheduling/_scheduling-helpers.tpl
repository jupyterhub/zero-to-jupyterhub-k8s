{{- /*
  jupyterhub.userTolerations
    Lists the tolerations for node taints that the user pods should have
*/}}
{{- define "jupyterhub.userTolerations" -}}
- key: hub.jupyter.org_dedicated
  operator: Equal
  value: user
  effect: NoSchedule
- key: hub.jupyter.org/dedicated
  operator: Equal
  value: user
  effect: NoSchedule
{{- if .Values.singleuser.extraTolerations }}
{{- .Values.singleuser.extraTolerations | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}



{{- define "jupyterhub.userNodeAffinityRequired" -}}
{{- if eq .Values.scheduling.userPods.nodeAffinity.matchNodePurpose "require" -}}
- matchExpressions:
  - key: hub.jupyter.org/node-purpose
    operator: In
    values: [user]
    {{- if .Values.singleuser.extraNodeAffinity.required }}{{ println }}{{ end }}
{{- end }}
{{- if .Values.singleuser.extraNodeAffinity.required -}}
{{ .Values.singleuser.extraNodeAffinity.required | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userNodeAffinityPreferred" -}}
{{- if eq .Values.scheduling.userPods.nodeAffinity.matchNodePurpose "prefer" -}}
- weight: 100
  preference:
    matchExpressions:
      - key: hub.jupyter.org/node-purpose
        operator: In
        values: [user]
        {{- if .Values.singleuser.extraNodeAffinity.preferred }}{{ println }}{{ end }}
{{- end }}
{{- if .Values.singleuser.extraNodeAffinity.preferred -}}
{{ .Values.singleuser.extraNodeAffinity.preferred | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userPodAffinityRequired" -}}
{{- if .Values.singleuser.extraPodAffinity.required -}}
{{ .Values.singleuser.extraPodAffinity.required | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userPodAffinityPreferred" -}}
{{- if .Values.singleuser.extraPodAffinity.preferred -}}
{{ .Values.singleuser.extraPodAffinity.preferred | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userPodAntiAffinityRequired" -}}
{{- if .Values.singleuser.extraPodAntiAffinity.required -}}
{{ .Values.singleuser.extraPodAntiAffinity.required | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}

{{- define "jupyterhub.userPodAntiAffinityPreferred" -}}
{{- if .Values.singleuser.extraPodAntiAffinity.preferred -}}
{{ .Values.singleuser.extraPodAntiAffinity.preferred | toYaml | trimSuffix "\n" }}
{{- end }}
{{- end }}



{{- define "jupyterhub.coreAffinity" -}}
{{- $require := eq .Values.scheduling.corePods.nodeAffinity.matchNodePurpose "require" -}}
{{- $prefer := eq .Values.scheduling.corePods.nodeAffinity.matchNodePurpose "prefer" -}}
{{- if or $require $prefer -}}
affinity:
  nodeAffinity:
    {{- if $require }}
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: hub.jupyter.org/node-purpose
            operator: In
            values: [core]
    {{- end }}
    {{- if $prefer }}
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
            - key: hub.jupyter.org/node-purpose
              operator: In
              values: [core]
    {{- end }}
{{- end }}
{{- end }}
