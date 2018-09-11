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
{{- if .podKind }}
{{- if eq .podKind "core" -}}
{{- $dummy := set . "matchNodePurpose" .Values.scheduling.corePods.nodeAffinity.matchNodePurpose }}
{{- else if eq .podKind "user" -}}
{{- $dummy := set . "matchNodePurpose" .Values.scheduling.userPods.nodeAffinity.matchNodePurpose }}
{{- end }}
{{- end }}

{{- $dummy := set . "tolerationsList" (include "jupyterhub.tolerationsList" .) }}
{{- $dummy := set . "tolerations" (include "jupyterhub.tolerations" .) }}
{{- $dummy := set . "hasTolerations" .tolerations }}

{{- $dummy := set . "nodeAffinityRequired" (include "jupyterhub.nodeAffinityRequired" .) }}
{{- $dummy := set . "podAffinityRequired" (include "jupyterhub.podAffinityRequired" .) }}
{{- $dummy := set . "podAntiAffinityRequired" (include "jupyterhub.podAntiAffinityRequired" .) }}
{{- $dummy := set . "nodeAffinityPreferred" (include "jupyterhub.nodeAffinityPreferred" .) }}
{{- $dummy := set . "podAffinityPreferred" (include "jupyterhub.podAffinityPreferred" .) }}
{{- $dummy := set . "podAntiAffinityPreferred" (include "jupyterhub.podAntiAffinityPreferred" .) }}
{{- $dummy := set . "hasNodeAffinity" (or .nodeAffinityRequired .nodeAffinityPreferred) }}
{{- $dummy := set . "hasPodAffinity" (or .podAffinityRequired .podAffinityPreferred) }}
{{- $dummy := set . "hasPodAntiAffinity" (or .podAntiAffinityRequired .podAntiAffinityPreferred) }}
{{- $dummy := set . "hasAffinity" (or .hasNodeAffinity .hasPodAffinity .hasPodAntiAffinity) }}

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



{{- define "jupyterhub.nodeAffinityRequired" -}}
{{- if eq .matchNodePurpose "require" -}}
- matchExpressions:
  - key: hub.jupyter.org/node-purpose
    operator: In
    values: [{{ .podKind }}]
{{- end }}
{{- if .Values.singleuser.extraNodeAffinity.required -}}
{{- .Values.singleuser.extraNodeAffinity.required | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}

{{- define "jupyterhub.nodeAffinityPreferred" -}}
{{- if eq .matchNodePurpose "prefer" -}}
- weight: 100
  preference:
    matchExpressions:
      - key: hub.jupyter.org/node-purpose
        operator: In
        values: [{{ .podKind }}]
{{- end }}
{{- if .Values.singleuser.extraNodeAffinity.preferred -}}
{{- .Values.singleuser.extraNodeAffinity.preferred | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}

{{- define "jupyterhub.podAffinityRequired" -}}
{{- if eq .podKind "core" -}}
{{- else if eq .podKind "user" -}}
{{- if .Values.singleuser.extraPodAffinity.required }}
{{- .Values.singleuser.extraPodAffinity.required | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}
{{- end }}

{{- define "jupyterhub.podAffinityPreferred" -}}
{{- if eq .podKind "core" -}}
{{- else if eq .podKind "user" -}}
{{- if .Values.scheduling.userPods.podAffinity.preferScheduleNextToRealUsers -}}
- weight: 100
  podAffinityTerm:
    labelSelector:
      matchExpressions:
        - key: component
          operator: In
          values: [singleuser-server]
    topologyKey: kubernetes.io/hostname
{{- end }}
{{- if .Values.singleuser.extraPodAffinity.preferred -}}
{{- .Values.singleuser.extraPodAffinity.preferred | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}
{{- end }}

{{- define "jupyterhub.podAntiAffinityRequired" -}}
{{- if eq .podKind "core" -}}
{{- else if eq .podKind "user" -}}
{{- if .Values.singleuser.extraPodAntiAffinity.required -}}
{{- .Values.singleuser.extraPodAntiAffinity.required | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}
{{- end }}

{{- define "jupyterhub.podAntiAffinityPreferred" -}}
{{- if eq .podKind "core" -}}
{{- else if eq .podKind "user" -}}
{{- if .Values.singleuser.extraPodAntiAffinity.preferred -}}
{{- .Values.singleuser.extraPodAntiAffinity.preferred | toYaml | trimSuffix "\n" | nindent 0 }}
{{- end }}
{{- end }}
{{- end }}



{{- /*
  input: podKind
*/}}
{{- define "jupyterhub.affinity" -}}
{{- if .hasAffinity -}}
affinity:
  {{- if .hasNodeAffinity }}
  nodeAffinity:
    {{- if .nodeAffinityRequired }}
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        {{- .nodeAffinityRequired | nindent 8 }}
    {{- end }}

    {{- if .nodeAffinityPreferred }}
    preferredDuringSchedulingIgnoredDuringExecution:
      {{- .nodeAffinityPreferred | nindent 6 }}
    {{- end }}
  {{- end }}

  {{- if .hasPodAffinity }}
  podAffinity:
    {{- if .podAffinityRequired }}
    requiredDuringSchedulingIgnoredDuringExecution:
      {{- .podAffinityRequired | nindent 6 }}
    {{- end }}

    {{- if .podAffinityPreferred }}
    preferredDuringSchedulingIgnoredDuringExecution:
      {{- .podAffinityPreferred | nindent 6 }}
    {{- end }}
  {{- end }}

  {{- if .hasPodAntiAffinity }}
  podAntiAffinity:
    {{- if .podAntiAffinityRequired }}
    requiredDuringSchedulingIgnoredDuringExecution:
      {{- .podAntiAffinityRequired | nindent 6 }}
    {{- end }}

    {{- if .podAntiAffinityPreferred }}
    preferredDuringSchedulingIgnoredDuringExecution:
      {{- .podAntiAffinityPreferred | nindent 6 }}
    {{- end }}
  {{- end }}
{{- end }}
{{- end }}
