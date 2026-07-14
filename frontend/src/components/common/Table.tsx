import React from 'react';
import Loader from './Loader';

export interface TableColumn<T> {
  key: string;
  header: string;
  render?: (row: T) => React.ReactNode;
}

interface TableProps<T> {
  columns: TableColumn<T>[];
  data: T[];
  isLoading?: boolean;
  emptyMessage?: string;
}

function Table<T>({ columns, data, isLoading = false, emptyMessage = 'No data available.' }: TableProps<T>) {
  return (
    <div className="w-full border border-slate-100 rounded-xl bg-white shadow-sm overflow-hidden font-sans">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-100">
              {columns.map((col) => (
                <th
                  key={col.key}
                  className="px-6 py-3.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider"
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-50">
            {isLoading ? (
              <tr>
                <td colSpan={columns.length} className="px-6 py-12 text-center">
                  <div className="flex justify-center items-center">
                    <Loader size="md" className="text-brand-500" />
                  </div>
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="px-6 py-12 text-center text-[13px] text-slate-400">
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              data.map((row: any, rowIndex) => (
                <tr key={row.id || rowIndex} className="hover:bg-slate-50/50 transition">
                  {columns.map((col) => (
                    <td key={col.key} className="px-6 py-4 text-[13px] text-slate-600 font-medium">
                      {col.render ? col.render(row) : row[col.key]}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Table;
