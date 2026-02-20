import React from 'react'

const ResponsiveTable = ({ headers, data, renderRow }) => {
  return (
    <div className="bg-white rounded-lg shadow overflow-x-auto">
      <table className="w-full">
        <thead className="bg-gray-50 border-b hidden-mobile">
          <tr>
            {headers.map((header, index) => (
              <th
                key={index}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
              >
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {data.length > 0 ? (
            data.map((item, index) => renderRow(item, index, headers))
          ) : (
            <tr>
              <td colSpan={headers.length} className="text-center py-8 text-gray-500">
                No data found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}

export default ResponsiveTable
