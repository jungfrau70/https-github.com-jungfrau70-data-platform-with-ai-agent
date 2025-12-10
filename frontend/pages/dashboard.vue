<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-2xl font-semibold text-gray-900">Data Analysis Dashboard</h1>
      
      <!-- Upload Section -->
      <div class="mt-8 bg-white overflow-hidden shadow sm:rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Upload Data</h3>
          <div class="mt-2 max-w-xl text-sm text-gray-500">
            <p>Upload a CSV, Excel, or Pickle file to generate an automated data summary.</p>
          </div>
          <div class="mt-5">
             <input type="file" @change="handleFileChange" accept=".csv,.xlsx,.pkl" class="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-primary
                hover:file:bg-blue-100" />
          </div>
          <div class="mt-3">
             <button @click="handleUpload" :disabled="!selectedFile || analysisStore.loading" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50">
               {{ analysisStore.loading ? 'Analyzing...' : 'Analyze' }}
             </button>
          </div>
          <div v-if="analysisStore.error" class="mt-2 text-red-600 text-sm">
             {{ analysisStore.error }}
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="analysisStore.summary" class="mt-8 space-y-8">
         <!-- Data Shape -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:px-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900">Dataset Overview</h3>
            </div>
            <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
                <dl class="sm:divide-y sm:divide-gray-200">
                    <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">Rows / Columns</dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ analysisStore.summary.shape[0] }} rows, {{ analysisStore.summary.shape[1] }} columns</dd>
                    </div>
                     <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                        <dt class="text-sm font-medium text-gray-500">Columns</dt>
                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ analysisStore.summary.columns.join(', ') }}</dd>
                    </div>
                </dl>
            </div>
        </div>

        <!-- Descriptive Stats -->
         <div class="bg-white shadow overflow-hidden sm:rounded-lg">
             <div class="px-4 py-5 sm:px-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900">Descriptive Statistics</h3>
            </div>
            <div class="border-t border-gray-200 p-4 overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Metric</th>
                             <th v-for="col in Object.keys(analysisStore.summary.describe)" :key="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                 {{ col }}
                             </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="metric in ['count', 'mean', 'std', 'min', 'max']" :key="metric">
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 capitalize">{{ metric }}</td>
                            <td v-for="col in Object.keys(analysisStore.summary.describe)" :key="col + metric" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {{ analysisStore.summary.describe[col][metric]?.toFixed(2) }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
         </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAnalysisStore } from '~/stores/analysis'

definePageMeta({
  middleware: ["auth"]
})

const analysisStore = useAnalysisStore()
const selectedFile = ref(null)

const handleFileChange = (event) => {
    selectedFile.value = event.target.files[0]
}

const handleUpload = async () => {
    if (!selectedFile.value) return
    await analysisStore.uploadFile(selectedFile.value)
}
</script>
