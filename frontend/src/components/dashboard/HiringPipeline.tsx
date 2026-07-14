import { useAppSelector } from '../../hooks';

interface PipelineStage {
  stage: string;
  count: number;
  colorClass: string;
}

const HiringPipeline: React.FC = () => {
  const { candidates } = useAppSelector((state) => state.candidates);
  const isEmpty = candidates.length === 0;

  // Static mockup database to render pipeline ratios
  const stages: PipelineStage[] = [
    { stage: 'Applied', count: isEmpty ? 0 : 48, colorClass: 'bg-brand-500' },
    { stage: 'Screening', count: isEmpty ? 0 : 24, colorClass: 'bg-blue-500' },
    { stage: 'Interviewing', count: isEmpty ? 0 : 12, colorClass: 'bg-yellow-500' },
    { stage: 'Offered', count: isEmpty ? 0 : 4, colorClass: 'bg-purple-500' },
    { stage: 'Hired', count: isEmpty ? 0 : 2, colorClass: 'bg-green-500' },
  ];

  const maxCount = Math.max(...stages.map((s) => s.count));

  return (
    <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm font-sans flex flex-col h-full">
      <h2 className="text-[14px] font-bold text-slate-800 tracking-tight mb-6">Hiring Funnel</h2>
      <div className="flex-1 flex flex-col justify-between gap-4">
        {stages.map((stage) => {
          const widthPercentage = maxCount > 0 ? (stage.count / maxCount) * 100 : 0;
          return (
            <div key={stage.stage} className="space-y-1.5">
              <div className="flex items-center justify-between text-[12px] font-medium text-slate-600">
                <span>{stage.stage}</span>
                <span className="font-bold text-slate-700">{stage.count}</span>
              </div>
              <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${stage.colorClass}`}
                  style={{ width: `${widthPercentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default HiringPipeline;
