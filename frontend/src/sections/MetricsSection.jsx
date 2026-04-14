import { Activity, DollarSign, TrendingDown, TrendingUp } from 'lucide-react';

import { MetricCard } from '../components/MetricCard';
import { formatCurrency } from '../utils/currency';

function buildDelta(current, reference, equalTooltip, aboveTooltip, belowTooltip) {
  if (current == null || reference == null) {
    return null;
  }

  return {
    current,
    reference,
    tooltip:
      current === reference
        ? equalTooltip
        : current > reference
          ? aboveTooltip
          : belowTooltip
  };
}


export function MetricsSection({ overallStats }) {
  return (
    <div className="metrics-grid">
      <MetricCard
        icon={<DollarSign size={22} />}
        label="Preço atual"
        value={formatCurrency(overallStats.current)}
        subtext={overallStats.currentStore}
        tone="blue"
      />
      <MetricCard
        icon={<TrendingDown size={22} />}
        label="Menor preço"
        value={formatCurrency(overallStats.min)}
        subtext={overallStats.minStore}
        tone="green"
        delta={buildDelta(
          overallStats.current,
          overallStats.min,
          'Preço atual está igual ao menor preço do período.',
          'Preço atual está acima do menor preço do período.',
          'Preço atual está abaixo do menor preço do período.'
        )}
      />
      <MetricCard
        icon={<TrendingUp size={22} />}
        label="Maior preço"
        value={formatCurrency(overallStats.max)}
        subtext={overallStats.maxStore}
        tone="red"
        delta={buildDelta(
          overallStats.current,
          overallStats.max,
          'Preço atual está igual ao maior preço do período.',
          'Preço atual está acima do maior preço do período.',
          'Preço atual está abaixo do maior preço do período.'
        )}
      />
      <MetricCard
        icon={<Activity size={22} />}
        label="Média do período"
        value={formatCurrency(overallStats.avg)}
        subtext="Entre lojas"
        tone="amber"
        delta={buildDelta(
          overallStats.current,
          overallStats.avg,
          'Preço atual está igual à média do período.',
          'Preço atual está acima da média do período.',
          'Preço atual está abaixo da média do período.'
        )}
      />
    </div>
  );
}
