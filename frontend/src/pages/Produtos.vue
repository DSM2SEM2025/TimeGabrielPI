<template>
  <div class="p-4 sm:p-6">
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4 sm:gap-6">
      <!-- Registro Manual -->
      <div class="bg-white rounded-xl shadow p-4 sm:p-6">
        <h2 class="text-lg font-semibold mb-4 sm:mb-6">Registro Manual de Produtos</h2>
        
        <form @submit.prevent="handleManualRegister" class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Nome do Produto
              </label>
              <input
                v-model="manualForm.name"
                type="text"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Categoria
              </label>
              <select
                v-model="manualForm.category"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              >
                <option value="">Selecione uma categoria</option>
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Descrição
            </label>
            <textarea
              v-model="manualForm.description"
              rows="3"
              class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
            ></textarea>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Quantidade Inicial
              </label>
              <input
                v-model="manualForm.initialQuantity"
                type="number"
                min="0"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Preço
              </label>
              <input
                v-model="manualForm.price"
                type="number"
                min="0"
                step="0.01"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Quantidade Mínima
              </label>
              <input
                v-model="manualForm.minQuantity"
                type="number"
                min="0"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Validade
              </label>
              <input
                v-model="manualForm.expiryDate"
                type="date"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Código da Nota Fiscal
              </label>
              <input
                v-model="manualForm.barcode"
                type="text"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Fornecedor
            </label>
            <input
              v-model="manualForm.supplier"
              type="text"
              class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
              required
            />
          </div>

          <div class="flex flex-col sm:flex-row justify-end gap-2 sm:gap-4 pt-4">
            <button
              type="button"
              @click="resetForm"
              class="w-full sm:w-auto px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 text-sm sm:text-base"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="w-full sm:w-auto px-4 py-2 text-white bg-purple-500 rounded-lg hover:bg-purple-600 text-sm sm:text-base"
            >
              Registrar Produto
            </button>
          </div>
        </form>
      </div>

      
      <!-- Registro Automatizado -->
      <div class="space-y-4 sm:space-y-6">
        <div class="bg-white rounded-xl shadow p-4 sm:p-6">
          <h2 class="text-lg font-semibold mb-4 sm:mb-6">Registro Automatizado de Produto</h2>

          <div class="flex flex-col space-y-4"> <div class="flex">
              <button
                @click="fazerBuscaEmail"
                :disabled="isLoadingEmail || isLoadingPdf"
                type="button" class="w-full sm:w-auto px-4 py-2 text-white bg-purple-500 rounded-lg hover:bg-purple-600 text-sm sm:text-base transition duration-300 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ isLoadingEmail ? "Buscando..." : "Fazer Busca no Email" }}
              </button>
            </div>

            <div class="flex">
              <button
                @click="inserirProdutosEstoque"
                :disabled="isLoadingEmail || isLoadingPdf"
                type="button" class="w-full sm:w-auto px-4 py-2 text-white bg-purple-500 rounded-lg hover:bg-purple-600 text-sm sm:text-base transition duration-300 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ isLoadingPdf ? "Inserindo..." : "Inserir Produtos no Estoque" }}
              </button>
            </div>
          </div>

          <div v-if="emailMessage.length > 0" :class="messageClass(emailStatus)" class="mt-4 p-3 rounded-md text-sm">
            {{ emailMessage }}
          </div>
          <div v-if="pdfMessage.length > 0" :class="messageClass(pdfStatus)" class="mt-4 p-3 rounded-md text-sm">
            {{ pdfMessage }}
          </div>
          <div v-if="pdfDetails.length > 0" class="mt-4 p-3 bg-gray-50 rounded-md text-sm max-h-48 overflow-y-auto">
            <h4 class="font-semibold mb-2">Detalhes do Processamento:</h4>
            <ul>
              <li v-for="(item, index) in pdfDetails" :key="index" class="mb-1">
                - PDF: {{ item.nome_arquivo_pdf || 'N/A' }}, Produto: {{ item.nome_produto || 'N/A' }}
              </li>
            </ul>
          </div>
        </div>
      </div>










      <!-- <div class="space-y-4 sm:space-y-6">
        <div class="bg-white rounded-xl shadow p-4 sm:p-6">
          <h2 class="text-lg font-semibold mb-4 sm:mb-6">Registro Automatizado de Produto</h2>

            <div class="flex">
              <button
                type="submit"
                class="w-full sm:w-auto px-4 py-2 text-white bg-purple-500 rounded-lg hover:bg-purple-600 text-sm sm:text-base"
              >
                Fazer Busca no Email
              </button>
            </div>

            <br>

            <div class="flex">
              <button
                type="submit"
                class="w-full sm:w-auto px-4 py-2 text-white bg-purple-500 rounded-lg hover:bg-purple-600 text-sm sm:text-base"
              >
                Inserir Produtos no Estoque
              </button>
            </div>
        </div> -->

        <!-- "Como funciona" -->
        <!-- <div class="bg-blue-50 rounded-xl p-4 sm:p-6">
          <h3 class="font-semibold mb-4">Como funciona:</h3>
          <ul class="space-y-3 sm:space-y-4">
            <li class="flex items-start">
              <div class="flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 mr-3">
                <span class="text-sm sm:text-base">1</span>
              </div>
              <p class="text-sm sm:text-base">Clique no botão 'Fazer Busca no Email'</p>
            </li>
            <li class="flex items-start">
              <div class="flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 mr-3">
                <span class="text-sm sm:text-base">2</span>
              </div>
              <p class="text-sm sm:text-base">O sistema automaticamente filtra seu email para encontrar possíveis Notas Fiscais</p>
            </li>
            <li class="flex items-start">
              <div class="flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 mr-3">
                <span class="text-sm sm:text-base">3</span>
              </div>
              <p class="text-sm sm:text-base">Caso tenham, clicando no botão 'Inserir Produtos no Estoque' eles são cadastrados automaticamentte no sistema</p>
            </li>
          </ul>
        </div>
      </div> -->
      
      
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();
const categories = ["Alimentos", "Bebidas", "Laticínios"];

const manualForm = ref({
  name: '',
  category: '',
  description: '',
  initialQuantity: 0,
  price: 0,
  minQuantity: 1,
  expiryDate: '',
  barcode: '',
  supplier: ''
});

const automatedForm = ref({
  invoiceLink: ''
});

const handleManualRegister = async () => {
  try {
    // Verifique se todos os campos obrigatórios estão preenchidos
    if (!manualForm.value.name || !manualForm.value.category || manualForm.value.initialQuantity <= 0) {
      alert('Por favor, preencha todos os campos obrigatórios!');
      return;
    }

    const produto = {
      nome_produto: manualForm.value.name,
      preco_produto: manualForm.value.price,
      desc_produto: manualForm.value.description,
      numero_nf_produto: manualForm.value.barcode,
      validade_produto: manualForm.value.expiryDate ? new Date(manualForm.value.expiryDate).toISOString().split('T')[0] : null,
      fornecedor_produto: manualForm.value.supplier,
      qtd_minima_produto: manualForm.value.minQuantity,
    };

    const estoque = {
      categoria_estoque: manualForm.value.category,
      qtde_estoque: manualForm.value.initialQuantity,
    };

    console.log("Enviando:", { produto, estoque });

    const response = await api.post('/produto', {
      produto, 
      estoque
    });

    alert('Produto cadastrado com sucesso!');
    resetForm();
    router.push('/estoque'); // Redireciona para a página de estoque após cadastro
  } catch (error) {
    console.error(error);
    if (error.response && error.response.data && error.response.data.detail) {
      alert(error.response.data.detail);
    } else {
      alert('Erro ao cadastrar produto. Verifique o console para mais detalhes.');
    }
  }
};

const handleAutomatedRegister = () => {
  // Implementar lógica de registro automatizado
  //Aqui entra o backend
  console.log('Link da nota fiscal:', automatedForm.value.invoiceLink);
};

const resetForm = () => {
  if (confirm('Deseja apagar os dados diigtados?')) {
    manualForm.value = {
      name: '',
      category: '',
      description: '',
      initialQuantity: 0,
      price: 0,
      minQuantity: 1,
      expiryDate: '',
      barcode: '',
      supplier: ''
    };
  }
};
const isLoadingEmail = ref(false);
const emailMessage = ref('');
const emailStatus = ref(''); // 'success', 'error', 'info'

// Estado para o processamento de PDFs
const isLoadingPdf = ref(false);
const pdfMessage = ref('');
const pdfStatus = ref(''); // 'success', 'error', 'info'
const pdfDetails = ref([]); // Para armazenar os detalhes_processamento se houver

// Helper para determinar a classe CSS da mensagem
const messageClass = (status) => {
  if (status === 'success') {
    return 'bg-green-100 text-green-700';
  } else if (status === 'error') {
    return 'bg-red-100 text-red-700';
  } else if (status === 'info') {
    return 'bg-blue-100 text-blue-700';
  }
  return ''; // Nenhuma classe se o status não for definido
};

// Função para obter o token JWT do usuário
// VERIFIQUE SE SEU `api` EM '@/services/api' JÁ ADICIONA O TOKEN AUTOMATICAMENTE
// via um interceptor. Se sim, você pode remover esta função e as linhas de 'const token = getAuthToken();'
const getAuthToken = () => {
  const token = localStorage.getItem("access_token"); // Exemplo: pegando do localStorage
  if (!token) {
    console.error("Token de autenticação não encontrado.");
    alert("Você precisa estar logado para realizar esta ação.");
    router.push('/login'); // Redirecionar para login
    return null;
  }
  return token;
};

// Função para chamar o endpoint de coleta de e-mails
const fazerBuscaEmail = async () => {
  isLoadingEmail.value = true;
  emailMessage.value = "";
  emailStatus.value = "";
  pdfDetails.value = []; // Limpa detalhes de PDFs anteriores

  // Descomente se seu 'api' NÃO adiciona o token automaticamente
  // const token = getAuthToken();
  // if (!token) {
  //   isLoadingEmail.value = false;
  //   return;
  // }

  try {
    // AJUSTE O CAMINHO: Se seu `api` já tem base "http://localhost:8000/api",
    // a rota completa será "/automacao/coletar-emails".
    const response = await api.get('/coletar-emails' /* , { headers: { Authorization: `Bearer ${token}` }} */);

    emailMessage.value = response.data.mensagem;
    emailStatus.value = response.data.status;

  } catch (error) {
    console.error("Erro na busca de e-mails:", error);
    if (error.response && error.response.data && error.response.data.detail) {
      emailMessage.value = `Erro: ${error.response.data.detail}`;
    } else {
      emailMessage.value = `Erro de conexão: ${error.message}. Verifique a API.`;
    }
    emailStatus.value = "error";
  } finally {
    isLoadingEmail.value = false;
  }
};

// Função para chamar o endpoint de processamento de PDFs
const inserirProdutosEstoque = async () => {
  isLoadingPdf.value = true;
  pdfMessage.value = "";
  pdfStatus.value = "";
  pdfDetails.value = [];


  try {

    //const response = await api.post('/processar-pdfs' /* , { headers: { Authorization: `Bearer ${token}` }} */);
    const response = await api.post('/processar-pdfs');

    pdfMessage.value = response.data.mensagem;
    pdfStatus.value = response.data.status;
    if (response.data.detalhes_processamento && Array.isArray(response.data.detalhes_processamento)) {
      pdfDetails.value = response.data.detalhes_processamento;
    }

  } catch (error) {
    console.error("Erro na inserção de produtos:", error);
    if (error.response && error.response.data && error.response.data.detail) {
      pdfMessage.value = `Erro: ${error.response.data.detail}`;
    } else {
      pdfMessage.value = `Erro de conexão: ${error.message}. Verifique a API.`;
    }
    pdfStatus.value = "error";
  } finally {
    isLoadingPdf.value = false;
  }
};


</script>