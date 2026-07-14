import { useAppSelector } from '../../hooks';

interface SkillStat {
  skillName: string;
  percentage: number;
}

const SkillChart: React.FC = () => {
  const { candidates } = useAppSelector((state) => state.candidates);

  if (candidates.length === 0) {
    return (
      <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm font-sans flex flex-col justify-center items-center h-48 text-center text-slate-400">
        <p className="text-xs font-semibold">No skills parsed yet.</p>
        <p className="text-[10px] text-slate-400 mt-1">Upload a candidate's resume to see skills stats breakdown.</p>
      </div>
    );
  }

  const topSkills: SkillStat[] = [
    { skillName: 'Python', percentage: 92 },
    { skillName: 'FastAPI', percentage: 85 },
    { skillName: 'React', percentage: 78 },
    { skillName: 'PostgreSQL', percentage: 70 },
    { skillName: 'Docker', percentage: 65 },
  ];

  return (
    <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm font-sans flex flex-col h-full">
      <h2 className="text-[14px] font-bold text-slate-800 tracking-tight mb-6">Top Parsed Skills</h2>
      <div className="flex-1 flex flex-col justify-between gap-4">
        {topSkills.map((skill) => (
          <div key={skill.skillName} className="space-y-1.5">
            <div className="flex items-center justify-between text-[12px] font-medium text-slate-600">
              <span className="font-semibold text-slate-700">{skill.skillName}</span>
              <span>{skill.percentage}% matched</span>
            </div>
            <div className="h-2 w-full bg-brand-50 rounded-full overflow-hidden">
              <div
                className="h-full bg-brand-500 rounded-full transition-all duration-500"
                style={{ width: `${skill.percentage}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SkillChart;
