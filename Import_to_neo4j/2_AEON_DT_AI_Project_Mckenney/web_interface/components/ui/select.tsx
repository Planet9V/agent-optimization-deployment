import * as React from 'react';

export type SelectProps = React.SelectHTMLAttributes<HTMLSelectElement>;

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className = '', children, ...props }, ref) => {
    return (
      <select
        className={`flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
        ref={ref}
        {...props}
      >
        {children}
      </select>
    );
  }
);

Select.displayName = 'Select';

// Compound component aliases for shadcn/ui compatibility
const SelectTrigger = Select;
const SelectValue = React.Fragment;
const SelectContent = React.Fragment;
const SelectItem = ({ children, value, ...props }: React.OptionHTMLAttributes<HTMLOptionElement>) => (
  <option value={value} {...props}>
    {children}
  </option>
);

export { Select, SelectTrigger, SelectValue, SelectContent, SelectItem };
