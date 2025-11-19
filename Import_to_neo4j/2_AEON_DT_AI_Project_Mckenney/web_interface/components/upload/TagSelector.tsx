"use client";

import { Badge } from "@tremor/react";

interface TagSelectorProps {
  selected: string[];
  onChange: (tags: string[]) => void;
}

interface Tag {
  id: string;
  label: string;
  color: "red" | "orange" | "blue" | "purple" | "green" | "gray";
}

const PREDEFINED_TAGS: Tag[] = [
  { id: "critical", label: "Critical", color: "red" },
  { id: "confidential", label: "Confidential", color: "orange" },
  { id: "technical", label: "Technical", color: "blue" },
  { id: "compliance", label: "Compliance", color: "purple" },
  { id: "financial", label: "Financial", color: "green" },
  { id: "operational", label: "Operational", color: "gray" },
];

export default function TagSelector({ selected, onChange }: TagSelectorProps) {
  const handleTagToggle = (tagId: string) => {
    if (selected.includes(tagId)) {
      // Deselect tag
      onChange(selected.filter((id) => id !== tagId));
    } else if (selected.length < 5) {
      // Select tag if under limit
      onChange([...selected, tagId]);
    }
  };

  const isSelected = (tagId: string) => selected.includes(tagId);
  const isDisabled = (tagId: string) => !isSelected(tagId) && selected.length >= 5;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100">
          Add Tags (Optional)
        </h3>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          {selected.length}/5 tags selected
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {PREDEFINED_TAGS.map((tag) => {
          const selected = isSelected(tag.id);
          const disabled = isDisabled(tag.id);

          return (
            <button
              key={tag.id}
              type="button"
              onClick={() => handleTagToggle(tag.id)}
              disabled={disabled}
              className={`
                transition-all duration-150 ease-in-out
                ${disabled ? "cursor-not-allowed opacity-40" : "cursor-pointer hover:scale-105"}
              `}
            >
              <Badge
                color={tag.color}
                size="lg"
                className={`
                  ${
                    selected
                      ? "ring-2 ring-offset-2 ring-offset-white dark:ring-offset-gray-950"
                      : "opacity-70 hover:opacity-100"
                  }
                `}
              >
                {tag.label}
              </Badge>
            </button>
          );
        })}
      </div>

      {selected.length === 5 && (
        <p className="text-xs text-amber-600 dark:text-amber-400">
          Maximum number of tags selected. Deselect a tag to choose another.
        </p>
      )}
    </div>
  );
}
