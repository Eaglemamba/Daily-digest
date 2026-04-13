// Dashboard data — each digest entry is added here after generation
// To add a new digest: append an object to the array below
const digests = [
  {
    date: '2026-04-13',
    dayOfWeek: 'Sunday',
    articles: 4,
    sources: ['HBR', 'AI Maker'],
    sourcesCount: 2,
    domains: ['hbr-review', 'ai-articles'],
    categories: ['Strategy', 'Leadership', 'AI'],
    lightNewsDay: true,
    file: 'digests/2026-04/digest-2026-04-13.html'
  },
  {
    date: '2026-04-12',
    dayOfWeek: 'Saturday',
    articles: 14,
    sources: ['Endpoints News', 'BioPharma Dive', 'Leadership in Change'],
    sourcesCount: 3,
    domains: ['pharma-decipher', 'hbr-review'],
    categories: ['FDA+', 'Deals', 'Clinical', 'Financing', 'Pipeline', 'Policy', 'Leadership'],
    lightNewsDay: false,
    file: 'digests/2026-04/digest-2026-04-12.html'
  }
];

// All 10 monitored newsletter sources
const allSources = [
  'Endpoints News', 'BioPharma Dive', 'HBR', 'Leadership in Change',
  'Department of Product', 'Ali Abdaal', 'AI Maker', 'Import AI', 'The Batch', 'PDA'
];

// Domain → display name + color mapping
const domainMeta = {
  'pharma-decipher': { label: 'Pharma', color: '#ef4444', bgClass: 'bg-red-50 text-red-700 border-red-200' },
  'hbr-review':      { label: 'Leadership', color: '#6366f1', bgClass: 'bg-indigo-50 text-indigo-700 border-indigo-200' },
  'ai-articles':     { label: 'AI', color: '#06b6d4', bgClass: 'bg-cyan-50 text-cyan-700 border-cyan-200' }
};

// Category badge color mapping
const categoryColors = {
  'FDA+':       'bg-red-50 text-red-700 border-red-200',
  'Deals':      'bg-green-50 text-green-700 border-green-200',
  'Clinical':   'bg-blue-50 text-blue-700 border-blue-200',
  'Financing':  'bg-purple-50 text-purple-700 border-purple-200',
  'Pipeline':   'bg-orange-50 text-orange-700 border-orange-200',
  'Policy':     'bg-gray-100 text-gray-700 border-gray-300',
  'Strategy':   'bg-indigo-50 text-indigo-700 border-indigo-200',
  'Leadership': 'bg-pink-50 text-pink-700 border-pink-200',
  'AI':         'bg-cyan-50 text-cyan-700 border-cyan-200',
  'Product':    'bg-violet-50 text-violet-700 border-violet-200',
  'Productivity': 'bg-amber-50 text-amber-700 border-amber-200'
};
