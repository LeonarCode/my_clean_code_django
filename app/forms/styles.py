"""Shared Tailwind classes for form widgets, so every form across the app looks consistent."""

INPUT_CLASSES = (
    "block w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm "
    "text-slate-900 placeholder:text-slate-400 shadow-sm transition "
    "focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/30 "
    "dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:placeholder:text-slate-500"
)

SELECT_CLASSES = INPUT_CLASSES + " appearance-none pr-10"

FILE_CLASSES = (
    "block w-full text-sm text-slate-600 dark:text-slate-300 "
    "file:mr-4 file:rounded-lg file:border-0 file:bg-teal-50 file:px-4 file:py-2 "
    "file:text-sm file:font-medium file:text-teal-700 hover:file:bg-teal-100 "
    "dark:file:bg-teal-500/10 dark:file:text-teal-300 dark:hover:file:bg-teal-500/20"
)

CHECKBOX_CLASSES = (
    "h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-2 focus:ring-teal-500/30 "
    "dark:border-slate-700 dark:bg-slate-800"
)
