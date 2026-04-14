import { Store } from 'lucide-react';

import { EmptyPanel } from '../components/EmptyPanel';
import { StoreCard } from '../components/StoreCard';

export function StoreComparisonSection({ storeStats, selectedProductName }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Comparação</p>
          <h2>Resumo por loja</h2>
        </div>
      </div>

      {storeStats.length ? (
        <div className="store-grid">
          {storeStats.map((store) => (
            <StoreCard
              key={store.storeName}
              store={store}
              productName={selectedProductName}
            />
          ))}
        </div>
      ) : (
        <EmptyPanel
          icon={<Store size={40} />}
          title="Sem cards por loja"
          description="Os cards aparecem quando o produto possui histórico no período selecionado."
        />
      )}
    </section>
  );
}
