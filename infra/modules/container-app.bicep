@description('Container App name')
param name string

@description('Azure region')
param location string

@description('Azure OpenAI endpoint')
param openaiEndpoint string

@description('Azure AI Search endpoint')
param searchEndpoint string

@description('Application Insights connection string')
param appInsightsConnectionString string

resource env 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: '${name}-env'
  location: location
  properties: {}
}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: name
  location: location
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
      }
      secrets: [
        { name: 'openai-endpoint', value: openaiEndpoint }
        { name: 'search-endpoint', value: searchEndpoint }
        { name: 'appinsights-cs', value: appInsightsConnectionString }
      ]
    }
    template: {
      containers: [
        {
          name: 'hu-ai-platform'
          image: 'ghcr.io/hilariopedro/hu-ai-platform-demo:latest'
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            { name: 'AZURE_OPENAI_ENDPOINT', secretRef: 'openai-endpoint' }
            { name: 'AZURE_SEARCH_ENDPOINT', secretRef: 'search-endpoint' }
            { name: 'OTEL_ENABLED', value: 'true' }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 3
      }
    }
  }
}

output url string = 'https://${app.properties.configuration.ingress.fqdn}'
