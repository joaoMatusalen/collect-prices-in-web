import { useEffect, useState } from 'react';
import { RefreshCcw } from 'lucide-react';

import { NoticeBanner } from './components/NoticeBanner';
import { ProductChart } from './components/ProductChart';
import { ThemeToggle } from './components/ThemeToggle';
import { ProductEditModal } from './components/modals/ProductEditModal';
import { ProductFormModal } from './components/modals/ProductFormModal';
import { ProductLinksModal } from './components/modals/ProductLinksModal';
import { useProductAnalytics } from './hooks/useProductAnalytics';
import { useProductEdit } from './hooks/useProductEdit';
import { useProductLinks } from './hooks/useProductLinks';
import { useProductList } from './hooks/useProductList';
import { useTheme } from './hooks/useTheme';
import { HeroPanel } from './sections/HeroPanel';
import { MetricsSection } from './sections/MetricsSection';
import { StoreComparisonSection } from './sections/StoreComparisonSection';

export default function App() {
  const { theme, toggle: toggleTheme, isDark } = useTheme();
  const [notice, setNotice] = useState(null);
  const [timeRange, setTimeRange] = useState('30');
  const [selectedStore, setSelectedStore] = useState('all');
  const [isProductFormOpen, setIsProductFormOpen] = useState(false);
  const [isProductEditOpen, setIsProductEditOpen] = useState(false);
  const [isProductLinksOpen, setIsProductLinksOpen] = useState(false);

  const {
    products,
    productOptions,
    selectedProduct,
    setSelectedProduct,
    selectedProductData,
    loadingProducts,
    submittingProduct,
    deletingProduct,
    loadProducts,
    handleProductSubmit: submitProduct,
    handleProductDelete: deleteProduct
  } = useProductList(setNotice);

  const {
    productUrls,
    newLink,
    setNewLink,
    linkDrafts,
    loadingUrls,
    submittingLink,
    savingLinkId,
    deletingLinkId,
    linksSummary,
    loadProductUrls,
    handleAddLink,
    handleSaveLink,
    handleDeleteLink,
    updateLinkDraft
  } = useProductLinks({ selectedProduct, setNotice });

  const {
    productEdit,
    savingProduct,
    updateProductEditField,
    handleProductUpdate: updateProduct
  } = useProductEdit({ selectedProductData, setNotice });

  const {
    filteredData,
    overallStats,
    selectedProductLabel,
    storeStats,
    loadingAnalytics,
    refetchAnalytics
  } = useProductAnalytics({
    timeRange,
    storeFilter: selectedStore,
    selectedProductData
  });

  useEffect(() => {
    setSelectedStore('all');
  }, [selectedProduct]);

  async function refreshSelectedProductData(productId = selectedProduct) {
    if (!productId) {
      return;
    }
    await Promise.all([loadProductUrls(productId), loadProducts(productId)]);
  }

  function handleRefresh() {
    refreshSelectedProductData();
    refetchAnalytics();
  }

  function handleProductSubmit(payload) {
    return submitProduct(payload, { refreshSelectedProductData });
  }

  function handleProductUpdate() {
    return updateProduct(loadProducts);
  }

  function handleProductDelete() {
    return deleteProduct(selectedProductData);
  }

  const heroActions = (
    <>
      <ProductFormModal
        products={products}
        onSubmit={handleProductSubmit}
        submitting={submittingProduct}
        open={isProductFormOpen}
        onOpenChange={setIsProductFormOpen}
      />
      <ProductEditModal
        selectedProductData={selectedProductData}
        productEdit={productEdit}
        onFieldChange={updateProductEditField}
        onSubmit={handleProductUpdate}
        onDelete={handleProductDelete}
        deletingProduct={deletingProduct}
        saving={savingProduct}
        open={isProductEditOpen}
        onOpenChange={setIsProductEditOpen}
      />
      <ProductLinksModal
        selectedProductData={selectedProductData}
        productUrls={productUrls}
        loadingUrls={loadingUrls}
        newLink={newLink}
        onNewLinkChange={setNewLink}
        linkDrafts={linkDrafts}
        onLinkDraftChange={updateLinkDraft}
        onAddLink={handleAddLink}
        onSaveLink={handleSaveLink}
        onDeleteLink={handleDeleteLink}
        submittingLink={submittingLink}
        savingLinkId={savingLinkId}
        deletingLinkId={deletingLinkId}
        open={isProductLinksOpen}
        onOpenChange={setIsProductLinksOpen}
      />
      <button
        type="button"
        className="secondary-button"
        onClick={handleRefresh}
        disabled={!selectedProduct || loadingUrls || loadingProducts || loadingAnalytics}
      >
        <RefreshCcw size={16} />
        Atualizar
      </button>
    </>
  );

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="topbar-kicker">Monitoramento de preço</p>
          <h1>Collect prices</h1>
          <p className="topbar-subtitle">
            Cadastre produtos, gerencie links por loja e acompanhe o histórico com comparativos mais claros.
          </p>
        </div>
        <ThemeToggle theme={theme} onToggle={toggleTheme} />
      </header>

      <NoticeBanner notice={notice} onDismiss={() => setNotice(null)} />

      <HeroPanel
        actions={heroActions}
        filteredSamplesCount={filteredData.length}
        linksSummary={linksSummary}
        loadingAnalytics={loadingAnalytics}
        loadingProducts={loadingProducts}
        onSelectedProductChange={setSelectedProduct}
        onSelectedStoreChange={setSelectedStore}
        onTimeRangeChange={setTimeRange}
        productOptions={productOptions}
        selectedProduct={selectedProduct}
        selectedProductLabel={selectedProductLabel}
        selectedStore={selectedStore}
        storeStats={storeStats}
        timeRange={timeRange}
      />

      <main className="content-grid">
        <section className="analytics-column">
          <MetricsSection overallStats={overallStats} />

          <ProductChart
            filteredData={filteredData}
            isDark={isDark}
            loadingHistory={loadingAnalytics}
            selectedProductData={selectedProductData}
            timeRange={timeRange}
          />

          <StoreComparisonSection
            storeStats={storeStats}
            selectedProductName={selectedProductData?.name}
          />
        </section>
      </main>
    </div>
  );
}
