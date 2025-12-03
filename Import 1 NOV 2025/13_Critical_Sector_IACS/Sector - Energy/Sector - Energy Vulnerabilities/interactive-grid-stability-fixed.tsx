import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ChevronDown, ChevronUp, Info, BarChart2, AlertTriangle, Zap, Power, Activity, RefreshCw } from 'lucide-react';

const GridStabilityExplorer = () => {
  // State for interactive elements
  const [section, setSection] = useState('intro');
  const [inertiaValue, setInertiaValue] = useState(8000);
  const [disturbanceValue, setDisturbanceValue] = useState(500);
  const [gfmPenetration, setGfmPenetration] = useState(10);
  const [rocofValue, setRocofValue] = useState(0.375);
  const [frequencyNadir, setFrequencyNadir] = useState(49.85);
  const [isSimulationRunning, setIsSimulationRunning] = useState(false);
  const [simulationState, setSimulationState] = useState('stable');
  const [chartPoints, setChartPoints] = useState([]);
  const [expandedFaqs, setExpandedFaqs] = useState([]);
  const [blackoutDetails, setBlackoutDetails] = useState(null);
  
  // Generate synthetic frequency data for simulator
  const generateFrequencyData = () => {
    const newRocof = (disturbanceValue / (2 * inertiaValue / 1000)) * (1 - (gfmPenetration * 0.015));
    setRocofValue(parseFloat(newRocof.toFixed(3)));
    
    const newNadir = 50 - (disturbanceValue / (inertiaValue / 100)) + (gfmPenetration * 0.005);
    setFrequencyNadir(parseFloat(newNadir.toFixed(2)));
    
    // Generate chart data
    const points = [];
    const totalPoints = 60;
    const dampingFactor = 0.95 - (gfmPenetration * 0.005);
    let currentValue = 50;
    let direction = -1;
    let deviation = (50 - newNadir) * 1.2;
    
    for (let i = 0; i < totalPoints; i++) {
      if (i === 0) {
        points.push({ time: i, frequency: 50 });
      } else if (i < 3) {
        // Initial drop
        currentValue = currentValue - (newRocof * 0.3);
        points.push({ time: i, frequency: currentValue });
      } else {
        // Oscillation with damping
        if (i % 10 === 0) direction *= -1;
        deviation *= dampingFactor;
        currentValue = 50 + (deviation * direction);
        points.push({ time: i, frequency: currentValue });
      }
    }
    return points;
  };
  
  // Trigger simulation
  const runSimulation = () => {
    setIsSimulationRunning(true);
    const points = generateFrequencyData();
    setChartPoints(points);
    
    // Determine stability state
    if (rocofValue > 1.0) {
      setSimulationState('unstable');
    } else if (rocofValue > 0.5) {
      setSimulationState('warning');
    } else {
      setSimulationState('stable');
    }
    
    // Reset after animation completes
    setTimeout(() => {
      setIsSimulationRunning(false);
    }, 5000);
  };
  
  // Toggle FAQ expansion
  const toggleFaq = (index) => {
    if (expandedFaqs.includes(index)) {
      setExpandedFaqs(expandedFaqs.filter(i => i !== index));
    } else {
      setExpandedFaqs([...expandedFaqs, index]);
    }
  };
  
  // Show blackout details
  const showBlackoutDetails = (event) => {
    setBlackoutDetails(event);
  };
  
  // Close blackout details modal
  const closeBlackoutDetails = () => {
    setBlackoutDetails(null);
  };
  
  // Sample data for charts
  const syncGenData = [
    { year: 2015, capacity: 75 },
    { year: 2020, capacity: 65 },
    { year: 2025, capacity: 45 },
    { year: 2030, capacity: 30 },
    { year: 2035, capacity: 20 },
  ];
  
  const renewableData = [
    { year: 2015, solar: 5, wind: 15, hydro: 5 },
    { year: 2020, solar: 10, wind: 20, hydro: 5 },
    { year: 2025, solar: 20, wind: 30, hydro: 5 },
    { year: 2030, solar: 30, wind: 35, hydro: 5 },
    { year: 2035, solar: 40, wind: 35, hydro: 5 },
  ];
  
  const inertiaData = [
    { year: 2015, inertia: 100 },
    { year: 2020, inertia: 85 },
    { year: 2025, inertia: 60 },
    { year: 2030, inertia: 40 },
    { year: 2035, inertia: 25 },
  ];
  
  const blackoutEvents = [
    {
      id: 1,
      name: 'US Northeast Blackout',
      date: 'August 14, 2003',
      region: 'United States & Canada',
      affected: '55 million people',
      duration: 'Up to 2 days',
      cause: 'Transmission lines contacting trees, inadequate situational awareness',
      description: 'This massive blackout affected the Northeastern and Midwestern United States and Ontario, Canada. It was triggered by transmission lines contacting trees amid high power flows and inadequate vegetation management. The event cascaded due to failures in situational awareness, inadequate operator tools, and subsequent voltage collapse.',
      learnings: 'Highlighted the importance of vegetation management, operator training, and real-time monitoring systems. Led to mandatory reliability standards under NERC.',
      ibrFactor: 'Low - Traditional grid vulnerabilities'
    },
    {
      id: 2,
      name: 'South Australia Blackout',
      date: 'September 28, 2016',
      region: 'South Australia',
      affected: '1.7 million people',
      duration: 'Up to 2 weeks in some areas',
      cause: 'Severe storm, wind farm protection settings, high RoCoF',
      description: 'Triggered by a severe storm damaging multiple transmission lines, this event saw a massive loss of wind generation (445 MW) due to repeated voltage dips activating protection settings. The system experienced an extreme RoCoF (up to 6.1 Hz/s) with very high IBR penetration (48.36%) and record low inertia (3000 MW·s).',
      learnings: 'Demonstrated the importance of appropriate ride-through settings for IBRs and the need for synthetic inertia in high renewable penetration systems.',
      ibrFactor: 'Very High - Direct demonstration of IBR-related instability'
    },
    {
      id: 3,
      name: 'UK Blackout',
      date: 'August 9, 2019',
      region: 'United Kingdom',
      affected: 'Over 1 million people',
      duration: 'Several hours',
      cause: 'Lightning strike, cascading generation trips, RoCoF relay settings',
      description: 'Initiated by a lightning strike tripping a transmission line, this event quickly escalated due to the nearly simultaneous loss of a gas power station and an offshore wind farm, followed by the tripping of distributed generation due to RoCoF exceeding relay settings (0.135 Hz/s vs 0.125 Hz/s threshold).',
      learnings: 'Highlighted the impact of RoCoF sensitivity in a system with significant wind penetration and relatively low inertia. Led to revisions in protection settings and grid codes.',
      ibrFactor: 'High - Demonstrated RoCoF sensitivity issues'
    },
    {
      id: 4,
      name: 'Iberian Peninsula Blackout',
      date: 'April 28, 2025',
      region: 'Spain & Portugal',
      affected: '60 million people',
      duration: 'Up to 10 hours',
      cause: 'Inter-area oscillations, IBR penetration, limited interconnection',
      description: 'This widespread power outage affected mainland Spain and Portugal. Preliminary investigations indicate low-frequency oscillations between the Iberian Peninsula and the rest of the European grid, potentially related to the high penetration of renewable energy in Spain (56% of the power mix in 2024).',
      learnings: 'Ongoing investigation, but highlights vulnerabilities in systems with very high renewable penetration and limited interconnection to broader synchronous areas.',
      ibrFactor: 'Very High - Directly linked to renewable penetration'
    }
  ];
  
  const stabilityTypes = [
    {
      name: 'Synchronous Inertia',
      traditional: 'High, inherent in rotating masses',
      modern: 'Low and Variable (depends on IBR penetration)',
      implications: 'Reduced ability to buffer frequency deviations; faster RoCoF',
      icon: <RefreshCw size={24} />
    },
    {
      name: 'Rate of Change of Frequency (RoCoF)',
      traditional: 'Relatively Slow (typically <0.1 Hz/s)',
      modern: 'Potentially Very High (>1 Hz/s)',
      implications: 'Challenges control system response times; increases risk of protection tripping',
      icon: <Activity size={24} />
    },
    {
      name: 'Primary Frequency Control',
      traditional: 'Primarily from Synchronous Generator Governors',
      modern: 'Reduced contribution from SGs; potential contribution from IBRs (if enabled)',
      implications: 'Need for alternative/supplementary fast frequency response sources',
      icon: <RefreshCw size={24} />
    },
    {
      name: 'Fault Current Contribution',
      traditional: 'High, from Synchronous Generators',
      modern: 'Lower, limited by Inverter Capabilities',
      implications: 'Challenges for traditional protection system coordination and operation',
      icon: <Zap size={24} />
    }
  ];
  
  const gfmFeatures = [
    { name: 'Synthetic Inertia', value: 80 },
    { name: 'Voltage Support', value: 90 },
    { name: 'Black Start Capability', value: 75 },
    { name: 'System Strength', value: 70 },
    { name: 'Frequency Control', value: 85 }
  ];
  
  const faqs = [
    {
      question: 'What is RoCoF and why is it important?',
      answer: 'RoCoF (Rate of Change of Frequency) measures how quickly system frequency changes following a disturbance, measured in Hz/s. It is critically important in low-inertia systems because rapid frequency changes can trigger protection relays, stress equipment, and outpace control system responses. Managing RoCoF is essential for maintaining grid stability as renewable penetration increases.'
    },
    {
      question: 'How do Grid-Forming inverters differ from traditional inverters?',
      answer: 'Grid-Forming (GFM) inverters can establish their own voltage and frequency reference, while traditional Grid-Following (GFL) inverters detect and synchronize to an existing grid signal. This fundamental difference enables GFM inverters to provide synthetic inertia, voltage support, and even Black Start capability, making them crucial for stability in high-renewable systems.'
    },
    {
      question: 'What is Black Start and why is it becoming more challenging?',
      answer: 'Black Start is the process of restarting the power system after a complete shutdown without relying on external power sources. It is becoming more challenging because: 1) Traditional Black Start resources like coal plants are retiring, 2) Most IBRs cannot currently initiate a restart, 3) Low-inertia systems are more sensitive during the restoration process, and 4) Fuel assurance for gas-powered Black Start units can be problematic during widespread infrastructure failures.'
    },
    {
      question: 'How does HVDC transmission help with grid stability?',
      answer: 'High Voltage Direct Current (HVDC) transmission supports grid stability by enabling asynchronous interconnections between different grids, preventing disturbances from propagating between systems. It allows precise control of power flows, experiences lower losses over long distances, and is ideal for connecting remote renewable resources. HVDC can also support frequency regulation through controlled modulation of power transfer.'
    }
  ];

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-800 to-blue-900 text-white py-8">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4">The Unseen Current</h1>
          <h2 className="text-2xl mb-6">Navigating Grid Instability in an Era of Transition</h2>
          <p className="text-xl italic">By J. McKenney | May 7, 2025</p>
        </div>
      </header>
      
      {/* Alert banner for recent events */}
      <div className="bg-amber-100 border-l-4 border-amber-500 p-4">
        <div className="flex items-center">
          <AlertTriangle className="text-amber-600 mr-3" />
          <p className="text-amber-700">
            <span className="font-bold">Recent Event: </span>
            On April 28, 2025, Spain and Portugal experienced their worst blackout in history, affecting 60 million people. This demonstrates the urgent challenges discussed in this analysis.
          </p>
        </div>
      </div>
      
      {/* Navigation */}
      <nav className="bg-white shadow-md">
        <div className="container mx-auto px-4">
          <div className="flex flex-wrap">
            <button 
              onClick={() => setSection('intro')} 
              className={`px-4 py-4 font-medium ${section === 'intro' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-blue-500'}`}
            >
              Introduction
            </button>
            <button 
              onClick={() => setSection('stability')} 
              className={`px-4 py-4 font-medium ${section === 'stability' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-blue-500'}`}
            >
              Grid Stability
            </button>
            <button 
              onClick={() => setSection('blackouts')} 
              className={`px-4 py-4 font-medium ${section === 'blackouts' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-blue-500'}`}
            >
              Historical Blackouts
            </button>
            <button 
              onClick={() => setSection('solutions')} 
              className={`px-4 py-4 font-medium ${section === 'solutions' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-blue-500'}`}
            >
              Emerging Solutions
            </button>
            <button 
              onClick={() => setSection('simulator')} 
              className={`px-4 py-4 font-medium ${section === 'simulator' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-blue-500'}`}
            >
              Grid Simulator
            </button>
          </div>
        </div>
      </nav>
      
      {/* Main content */}
      <main className="flex-grow container mx-auto px-4 py-8">
        {/* Introduction Section */}
        {section === 'intro' && (
          <div>
            <h2 className="text-3xl font-bold mb-6">Our Unseen Lifeline: The Profound Reliance on Unwavering Electricity</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-center mb-4">
                  <Power className="text-blue-600" size={48} />
                </div>
                <h3 className="text-xl font-semibold text-center mb-2">Critical Infrastructure</h3>
                <p className="text-gray-700">Electricity powers our water systems, hospitals, transportation networks, and communication systems.</p>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-center mb-4">
                  <BarChart2 className="text-blue-600" size={48} />
                </div>
                <h3 className="text-xl font-semibold text-center mb-2">Economic Engine</h3>
                <p className="text-gray-700">Powers commerce, manufacturing, and the digital economy that drives prosperity.</p>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-center mb-4">
                  <Activity className="text-blue-600" size={48} />
                </div>
                <h3 className="text-xl font-semibold text-center mb-2">Social Fabric</h3>
                <p className="text-gray-700">Enables education, entertainment, and the connectivity that binds communities together.</p>
              </div>
            </div>
            
            <p className="text-lg mb-4">
              Electricity, often summoned with the mere flick of a switch, stands as a silent partner in nearly every facet of modern existence. This constant, reliable flow of energy is a legacy built over generations, a testament to our ability to harness nature and construct complex, life-sustaining systems.
            </p>
            
            <p className="text-lg mb-6">
              As our reliance deepens, particularly with the pervasive digitization of society, the consequences of failure magnify. A disruption that might have been a localized inconvenience decades ago can now trigger cascading effects across economic, social, and public safety domains.
            </p>
            
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-8">
              <p className="text-lg font-semibold text-blue-800">
                "Will our grandchildren inherit a world where these foundational elements are secure, powered by a resilient and reliable energy system? Or will they face a future characterized by increasing uncertainty, where the invisible current we mastered becomes a source of fragility?"
              </p>
            </div>
            
            <h3 className="text-2xl font-bold mb-4">The Changing Landscape of Power Generation</h3>
            
            <div className="mb-8 h-80">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={renewableData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis label={{ value: 'Percentage of Generation Mix', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="solar" stackId="1" stroke="#FFB74D" fill="#FFECB3" name="Solar" />
                  <Area type="monotone" dataKey="wind" stackId="1" stroke="#4FC3F7" fill="#B3E5FC" name="Wind" />
                  <Area type="monotone" dataKey="hydro" stackId="1" stroke="#4DB6AC" fill="#B2DFDB" name="Hydro" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            
            <p className="text-lg mb-8">
              The vital systems upon which we depend are exhibiting new forms of strain, novel fragilities born from the very transition intended to secure our energy future. The accelerating shift towards renewable energy sources, while indispensable for environmental stewardship, is fundamentally altering the physical characteristics and operational dynamics of the grid.
            </p>
            
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h3 className="text-xl font-semibold mb-4">System Inertia Decline with Renewable Integration</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={inertiaData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis domain={[0, 100]} label={{ value: 'Relative System Inertia (%)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Line type="monotone" dataKey="inertia" stroke="#2196F3" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <p className="text-gray-700 mt-4">
                As we replace synchronous generators with inverter-based resources, system inertia decreases, making the grid more vulnerable to rapid frequency changes.
              </p>
            </div>
          </div>
        )}
        
        {/* Grid Stability Section */}
        {section === 'stability' && (
          <div>
            <h2 className="text-3xl font-bold mb-6">The Precarious Balance: Understanding Grid Stability</h2>
            
            <p className="text-lg mb-4">
              The reliable operation of the electric power grid hinges on maintaining a continuous, instantaneous balance between electricity supply (generation) and demand (load). System frequency, typically standardized at 60 Hz in North America and 50 Hz in Europe, serves as the primary, real-time indicator of this delicate equilibrium.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold mb-4">Traditional Grid Stability</h3>
                <p className="mb-4">
                  For decades, the stability of power systems has relied on synchronous generators with large rotating masses that store kinetic energy. This property, known as synchronous inertia, acts as a natural shock absorber against disturbances.
                </p>
                <div className="bg-blue-50 p-4 rounded">
                  <h4 className="font-semibold mb-2">Key Properties:</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    <li>High inherent inertia from rotating masses</li>
                    <li>Slow rate of frequency change after disturbances</li>
                    <li>Governor response provides primary frequency control</li>
                    <li>Strong fault current contribution aids protection</li>
                  </ul>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold mb-4">Emerging Low-Inertia Challenges</h3>
                <p className="mb-4">
                  As we integrate more inverter-based resources like solar and wind, we're removing traditional sources of inertia, creating new stability challenges characterized by rapid frequency changes.
                </p>
                <div className="bg-amber-50 p-4 rounded">
                  <h4 className="font-semibold mb-2">Key Concerns:</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    <li>High Rate of Change of Frequency (RoCoF)</li>
                    <li>Control systems may not respond quickly enough</li>
                    <li>Protection relay misoperation risk increases</li>
                    <li>Equipment may experience higher mechanical stress</li>
                  </ul>
                </div>
              </div>
            </div>
            
            <h3 className="text-2xl font-bold mb-4">The 'Death Wobble': Understanding Frequency Instability</h3>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
              <div className="col-span-1 lg:col-span-2">
                <div className="h-64 bg-white rounded-lg shadow-md p-4">
                  <h4 className="font-semibold mb-2">Frequency Response Comparison</h4>
                  <ResponsiveContainer width="100%" height="90%">
                    <LineChart>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" domain={[0, 20]} label={{ value: 'Time (seconds)', position: 'insideBottom', offset: -5 }} />
                      <YAxis domain={[49.2, 50.2]} label={{ value: 'Frequency (Hz)', angle: -90, position: 'insideLeft' }} />
                      <Tooltip />
                      <Legend />
                      <Line name="High Inertia" type="monotone" data={[
                        {x: 0, y: 50}, {x: 1, y: 50}, 
                        {x: 2, y: 49.9}, {x: 3, y: 49.85}, 
                        {x: 4, y: 49.83}, {x: 5, y: 49.82}, 
                        {x: 6, y: 49.84}, {x: 7, y: 49.87}, 
                        {x: 8, y: 49.9}, {x: 9, y: 49.92}, 
                        {x: 10, y: 49.94}, {x: 11, y: 49.95}, 
                        {x: 12, y: 49.96}, {x: 13, y: 49.97}, 
                        {x: 14, y: 49.98}, {x: 15, y: 49.99}, 
                        {x: 16, y: 50}, {x: 17, y: 50}, 
                        {x: 18, y: 50}, {x: 19, y: 50}, {x: 20, y: 50}
                      ]} dataKey="y" xAxisId={0} stroke="#4CAF50" strokeWidth={3} />
                      <Line name="Low Inertia" type="monotone" data={[
                        {x: 0, y: 50}, {x: 1, y: 50}, 
                        {x: 2, y: 49.7}, {x: 3, y: 49.4}, 
                        {x: 4, y: 49.3}, {x: 5, y: 49.35}, 
                        {x: 6, y: 49.5}, {x: 7, y: 49.6}, 
                        {x: 8, y: 49.55}, {x: 9, y: 49.5}, 
                        {x: 10, y: 49.6}, {x: 11, y: 49.7}, 
                        {x: 12, y: 49.75}, {x: 13, y: 49.73}, 
                        {x: 14, y: 49.78}, {x: 15, y: 49.85}, 
                        {x: 16, y: 49.9}, {x: 17, y: 49.95}, 
                        {x: 18, y: 49.98}, {x: 19, y: 50}, {x: 20, y: 50}
                      ]} dataKey="y" xAxisId={0} stroke="#F44336" strokeWidth={3} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <h4 className="font-semibold mb-2">Frequency Response Metrics</h4>
                <div className="space-y-4">
                  <div>
                    <span className="text-gray-700 block mb-1">High Inertia System:</span>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">RoCoF:</span>
                      <span className="font-semibold">0.1 Hz/s</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Nadir:</span>
                      <span className="font-semibold">49.82 Hz</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Recovery Time:</span>
                      <span className="font-semibold">16 seconds</span>
                    </div>
                  </div>
                  
                  <div className="pt-4 border-t border-gray-200">
                    <span className="text-gray-700 block mb-1">Low Inertia System:</span>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">RoCoF:</span>
                      <span className="font-semibold text-red-600">0.6 Hz/s</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Nadir:</span>
                      <span className="font-semibold text-red-600">49.3 Hz</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Recovery Time:</span>
                      <span className="font-semibold">19 seconds</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <h3 className="text-2xl font-bold mb-4">Traditional vs. Modern Grid Characteristics</h3>
            
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <div className="overflow-x-auto">
                <table className="min-w-full bg-white">
                  <thead>
                    <tr>
                      <th className="py-3 px-4 bg-blue-50 text-left">Feature</th>
                      <th className="py-3 px-4 bg-blue-50 text-left">Traditional Grid</th>
                      <th className="py-3 px-4 bg-blue-50 text-left">Low-Inertia Grid</th>
                      <th className="py-3 px-4 bg-blue-50 text-left">Key Implications</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stabilityTypes.map((type, index) => (
                      <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                        <td className="py-3 px-4 border-b flex items-center">
                          {type.icon}
                          <span className="ml-2">{type.name}</span>
                        </td>
                        <td className="py-3 px-4 border-b">{type.traditional}</td>
                        <td className="py-3 px-4 border-b">{type.modern}</td>
                        <td className="py-3 px-4 border-b">{type.implications}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
        
        {/* Historical Blackouts Section */}
        {section === 'blackouts' && (
          <div>
            <h2 className="text-3xl font-bold mb-6">When the Lights Go Out: The Anatomy of Cascading Failures</h2>
            
            <p className="text-lg mb-4">
              A cascading failure is a sequence of dependent outages in a power system, where an initial triggering event leads to subsequent failures of other components, potentially culminating in a large-scale blackout. These events are among the most severe threats to grid reliability.
            </p>
            
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h3 className="text-xl font-semibold mb-4">Key Propagation Mechanisms</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="border rounded p-4">
                  <h4 className="font-medium text-lg mb-2">Line Overloads</h4>
                  <p>The loss of one transmission line forces power to reroute onto parallel paths, potentially overloading them beyond their thermal limits, leading to sagging, contact with vegetation, and subsequent tripping.</p>
                </div>
                
                <div className="border rounded p-4">
                  <h4 className="font-medium text-lg mb-2">Voltage Collapse</h4>
                  <p>Insufficient reactive power support following contingencies can lead to a progressive decline in voltage levels across an area, potentially causing loads to stall and generators to trip.</p>
                </div>
                
                <div className="border rounded p-4">
                  <h4 className="font-medium text-lg mb-2">Frequency Instability</h4>
                  <p>Large power imbalances in low-inertia systems can lead to rapid frequency deviations (high RoCoF) or sustained under/over-frequency conditions, triggering protective relays on generators and loads.</p>
                </div>
                
                <div className="border rounded p-4">
                  <h4 className="font-medium text-lg mb-2">Protection System Actions</h4>
                  <p>Hidden failures, incorrect settings, or the designed operation of protection systems can sometimes fail to isolate the initial problem or may even contribute to the cascade by unnecessarily tripping healthy equipment.</p>
                </div>
              </div>
            </div>
            
            <h3 className="text-2xl font-bold mb-4">Timeline of Major Blackouts</h3>
            
            <div className="relative">
              {/* Timeline line */}
              <div className="absolute h-full w-1 bg-blue-200 left-0 md:left-1/2 transform md:-translate-x-1/2"></div>
              
              {/* Timeline events */}
              {blackoutEvents.map((event, index) => (
                <div key={index} className={`relative mb-8 ${index % 2 === 0 ? 'md:ml-auto md:pl-8 md:pr-0 md:text-left' : 'md:mr-auto md:pr-8 md:pl-0 md:text-right'} 
                                           md:w-1/2 pl-8`}>
                  {/* Timeline dot */}
                  <div className="absolute w-4 h-4 bg-blue-500 rounded-full left-0 top-5 transform -translate-x-1.5 md:left-1/2 md:-translate-x-2"></div>
                  
                  {/* Content */}
                  <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow cursor-pointer"
                       onClick={() => showBlackoutDetails(event)}>
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 rounded-full mb-2">{event.date}</span>
                    <h4 className="text-lg font-semibold mb-1">{event.name}</h4>
                    <p className="text-gray-600 mb-2">Affected: {event.affected}</p>
                    <p className="text-gray-700 mb-2">Cause: {event.cause}</p>
                    <div className="flex items-center justify-between mt-2">
                      <span className={`inline-block px-2 py-1 rounded text-xs font-semibold
                                      ${event.ibrFactor.includes('Very High') 
                                        ? 'bg-red-100 text-red-800' 
                                        : event.ibrFactor.includes('High')
                                          ? 'bg-orange-100 text-orange-800'
                                          : 'bg-gray-100 text-gray-800'}`}>
                        {event.ibrFactor}
                      </span>
                      <span className="text-blue-600 text-sm">View Details →</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Blackout comparison chart */}
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h3 className="text-xl font-semibold mb-4">Blackout Impact Comparison</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={blackoutEvents}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis label={{ value: 'Relative Impact Score', angle: -90, position: 'insideLeft' }} />
                    <Tooltip 
                      formatter={(value, name, props) => {
                        if (name === 'ibrImpact') return [`${value}/10`, 'IBR Impact'];
                        return [value, name];
                      }}
                    />
                    <Legend />
                    <Bar name="People Affected (millions)" dataKey={(entry) => Number(entry.affected.split(' ')[0])} fill="#3F51B5" />
                    <Bar name="IBR Impact Factor" dataKey={(entry) => {
                      if (entry.ibrFactor.includes('Very High')) return 9;
                      if (entry.ibrFactor.includes('High')) return 7;
                      if (entry.ibrFactor.includes('Medium')) return 5;
                      if (entry.ibrFactor.includes('Low')) return 3;
                      return 1;
                    }} fill="#F44336" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
            
            {/* Blackout detail modal */}
            {blackoutDetails && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="text-2xl font-bold">{blackoutDetails.name}</h3>
                      <button 
                        className="text-gray-500 hover:text-gray-700" 
                        onClick={closeBlackoutDetails}
                      >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <span className="block text-sm text-gray-600">Date:</span>
                        <span className="font-medium">{blackoutDetails.date}</span>
                      </div>
                      <div>
                        <span className="block text-sm text-gray-600">Region:</span>
                        <span className="font-medium">{blackoutDetails.region}</span>
                      </div>
                      <div>
                        <span className="block text-sm text-gray-600">People Affected:</span>
                        <span className="font-medium">{blackoutDetails.affected}</span>
                      </div>
                      <div>
                        <span className="block text-sm text-gray-600">Duration:</span>
                        <span className="font-medium">{blackoutDetails.duration}</span>
                      </div>
                    </div>
                    
                    <div className="mb-4">
                      <h4 className="font-semibold mb-2">Cause</h4>
                      <p className="text-gray-700">{blackoutDetails.cause}</p>
                    </div>
                    
                    <div className="mb-4">
                      <h4 className="font-semibold mb-2">Description</h4>
                      <p className="text-gray-700">{blackoutDetails.description}</p>
                    </div>
                    
                    <div className="mb-4">
                      <h4 className="font-semibold mb-2">Key Learnings</h4>
                      <p className="text-gray-700">{blackoutDetails.learnings}</p>
                    </div>
                    
                    <div className="mt-6">
                      <h4 className="font-semibold mb-2">IBR Impact Assessment</h4>
                      <div className={`p-3 rounded-md ${
                        blackoutDetails.ibrFactor.includes('Very High') 
                          ? 'bg-red-50 text-red-700' 
                          : blackoutDetails.ibrFactor.includes('High')
                            ? 'bg-orange-50 text-orange-700'
                            : 'bg-gray-50 text-gray-700'
                      }`}>
                        <span className="font-medium">{blackoutDetails.ibrFactor}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
        
        {/* Emerging Solutions Section */}
        {section === 'solutions' && (
          <div>
            <h2 className="text-3xl font-bold mb-6">Charting a Resilient Trajectory: Innovations for a Secure Energy Future</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div>
                <h3 className="text-2xl font-bold mb-4">Grid-Forming Inverters</h3>
                <p className="mb-4">
                  Unlike conventional Grid-Following (GFL) inverters, Grid-Forming (GFM) inverters possess the control intelligence to establish their own voltage and frequency reference. This fundamental difference enables GFM inverters to provide critical grid services traditionally supplied by synchronous generators.
                </p>
                
                <div className="bg-white rounded-lg shadow-md p-6 mb-4">
                  <h4 className="font-semibold mb-4">GFM Capabilities Assessment</h4>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={gfmFeatures} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" domain={[0, 100]} />
                        <YAxis dataKey="name" type="category" width={140} />
                        <Tooltip />
                        <Bar dataKey="value" fill="#4CAF50">
                          {gfmFeatures.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.value > 75 ? '#4CAF50' : '#FFA726'} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">
                    Capability assessment based on current technology readiness levels and demonstrated performance in pilot projects.
                  </p>
                </div>
              </div>
              
              <div>
                <h3 className="text-2xl font-bold mb-4">HVDC Transmission</h3>
                <p className="mb-4">
                  High Voltage Direct Current (HVDC) technology plays a vital role in enabling and enhancing interconnections, offering several advantages over traditional HVAC transmission, particularly for long-distance power transfer and connecting asynchronous systems.
                </p>
                
                <div className="grid grid-cols-1 gap-4 mb-4">
                  <div className="bg-white rounded-lg shadow-md p-4">
                    <div className="flex items-center mb-2">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 mr-3">1</div>
                      <h4 className="font-semibold">Lower Transmission Losses</h4>
                    </div>
                    <p className="text-gray-700 pl-11">
                      HVDC lines experience significantly lower power losses over long distances, making them ideal for transmitting bulk power from remote renewable generation sites to load centers.
                    </p>
                  </div>
                  
                  <div className="bg-white rounded-lg shadow-md p-4">
                    <div className="flex items-center mb-2">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 mr-3">2</div>
                      <h4 className="font-semibold">Asynchronous Connections</h4>
                    </div>
                    <p className="text-gray-700 pl-11">
                      HVDC allows grids operating at different frequencies or grids that are not synchronized to be connected and exchange power, enhancing stability by preventing disturbances in one grid from directly propagating to the other.
                    </p>
                  </div>
                  
                  <div className="bg-white rounded-lg shadow-md p-4">
                    <div className="flex items-center mb-2">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 mr-3">3</div>
                      <h4 className="font-semibold">Precise Control</h4>
                    </div>
                    <p className="text-gray-700 pl-11">
                      HVDC links allow operators to precisely control the amount and direction of power flow, improving grid manageability and stability during dynamic events.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            
            <h3 className="text-2xl font-bold mb-4">Black Start Innovations</h3>
            
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h4 className="font-semibold mb-4">Evolution of Black Start Capabilities</h4>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div className="border-r pr-4">
                  <h5 className="font-medium mb-2">Traditional Approach</h5>
                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>Dedicated fossil fuel generators</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>Large hydroelectric plants</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>On-site fuel storage</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>Centralized command structure</span>
                    </li>
                  </ul>
                </div>
                
                <div className="border-r px-4">
                  <h5 className="font-medium mb-2">Current Challenges</h5>
                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <span className="text-red-600 mr-2">✗</span>
                      <span>Retirement of traditional units</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-red-600 mr-2">✗</span>
                      <span>IBRs lack inherent capability</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-red-600 mr-2">✗</span>
                      <span>Increased reliance on natural gas</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-red-600 mr-2">✗</span>
                      <span>Low-inertia complicates restoration</span>
                    </li>
                  </ul>
                </div>
                
                <div className="pl-4">
                  <h5 className="font-medium mb-2">Emerging Solutions</h5>
                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <span className="text-blue-600 mr-2">→</span>
                      <span>GFM inverters with BESS</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-blue-600 mr-2">→</span>
                      <span>Distributed Re-Start capabilities</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-blue-600 mr-2">→</span>
                      <span>Enhanced TSO-DNO collaboration</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-blue-600 mr-2">→</span>
                      <span>Diverse fuel/resource procurement</span>
                    </li>
                  </ul>
                </div>
              </div>
              
              <div className="h-64 mt-6">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={[
                        { name: 'Conventional Generation', value: 65, color: '#78909C' },
                        { name: 'Grid-Forming BESS', value: 15, color: '#4CAF50' },
                        { name: 'Hydroelectric', value: 10, color: '#42A5F5' },
                        { name: 'Other Innovative Resources', value: 10, color: '#FFA726' },
                      ]}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {[
                        { name: 'Conventional Generation', value: 65, color: '#78909C' },
                        { name: 'Grid-Forming BESS', value: 15, color: '#4CAF50' },
                        { name: 'Hydroelectric', value: 10, color: '#42A5F5' },
                        { name: 'Other Innovative Resources', value: 10, color: '#FFA726' },
                      ].map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <p className="text-sm text-gray-600 text-center mt-2">
                Projected Black Start Resource Mix for 2030
              </p>
            </div>
            
            <h3 className="text-2xl font-bold mb-4">Standards and Policy Developments</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h4 className="font-semibold mb-3">IEEE Standard 2800-2022</h4>
                <p className="text-gray-700 mb-3">
                  Establishes uniform minimum technical requirements for the interconnection and interoperability of large IBRs.
                </p>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>Fault and frequency ride-through capabilities</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>Reactive and active power control requirements</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>Performance targets for control functions</span>
                  </li>
                </ul>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <h4 className="font-semibold mb-3">NERC PRC-029-1</h4>
                <p className="text-gray-700 mb-3">
                  Establishes mandatory voltage and frequency ride-through requirements specifically for IBRs.
                </p>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>Defines "must ride-through" zones</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>Maximum allowable RoCoF limit: 5 Hz/second</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>Prohibits momentary cessation during disturbances</span>
                  </li>
                </ul>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <h4 className="font-semibold mb-3">ENTSO-E Framework</h4>
                <p className="text-gray-700 mb-3">
                  Develops network codes and guidelines addressing frequency stability and inertia management in Europe.
                </p>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>Frequency quality requirements</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>RoCoF limits (>1 Hz/s potentially unmanageable)</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>System defense and emergency measures</span>
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h4 className="text-xl font-semibold mb-4">Beyond Technology: The Human Element</h4>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h5 className="font-medium text-lg mb-3">Policy and Strategic Investment</h5>
                  <p className="text-gray-700 mb-3">
                    Effective policies must ensure resource adequacy in a changing generation mix, while market designs need to appropriately value essential reliability services like inertia and frequency response.
                  </p>
                  <p className="text-gray-700">
                    Massive, strategic investment is required not only in renewable generation but also in the enabling infrastructure: transmission expansion, energy storage, and grid modernization technologies.
                  </p>
                </div>
                
                <div>
                  <h5 className="font-medium text-lg mb-3">Workforce Development and Public Engagement</h5>
                  <p className="text-gray-700 mb-3">
                    The transition demands a significant focus on workforce development to ensure there are enough engineers, technicians, and operators skilled in designing and managing these complex new systems.
                  </p>
                  <p className="text-gray-700">
                    Public engagement is vital. Consumers and communities need to understand the challenges, the necessity of investments, and the benefits of a modernized, resilient grid.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Grid Simulator Section */}
        {section === 'simulator' && (
          <div>
            <h2 className="text-3xl font-bold mb-6">Interactive Grid Stability Simulator</h2>
            
            <p className="text-lg mb-6">
              Experiment with the interactive simulator below to see how different factors affect grid stability. Adjust system inertia, disturbance size, and grid-forming penetration to observe their impact on frequency response.
            </p>
            
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h3 className="text-xl font-semibold mb-4">RoCoF Simulator</h3>
              
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                <div className="bg-gray-50 p-4 rounded-md">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    System Inertia (GW·s)
                  </label>
                  <input
                    type="range"
                    min="2000"
                    max="15000"
                    value={inertiaValue}
                    onChange={(e) => setInertiaValue(Number(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between mt-2">
                    <span className="text-xs text-gray-600">Low (2000)</span>
                    <span className="text-sm font-semibold">{inertiaValue}</span>
                    <span className="text-xs text-gray-600">High (15000)</span>
                  </div>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-md">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Power Imbalance (MW)
                  </label>
                  <input
                    type="range"
                    min="100"
                    max="2000"
                    value={disturbanceValue}
                    onChange={(e) => setDisturbanceValue(Number(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between mt-2">
                    <span className="text-xs text-gray-600">Small (100)</span>
                    <span className="text-sm font-semibold">{disturbanceValue} MW</span>
                    <span className="text-xs text-gray-600">Large (2000)</span>
                  </div>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-md">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Grid-Forming Penetration (%)
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="50"
                    value={gfmPenetration}
                    onChange={(e) => setGfmPenetration(Number(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between mt-2">
                    <span className="text-xs text-gray-600">None (0%)</span>
                    <span className="text-sm font-semibold">{gfmPenetration}%</span>
                    <span className="text-xs text-gray-600">High (50%)</span>
                  </div>
                </div>
              </div>
              
              <div className="flex justify-center mb-6">
                <button
                  onClick={runSimulation}
                  disabled={isSimulationRunning}
                  className={`px-6 py-3 rounded-md font-semibold text-white 
                             ${isSimulationRunning ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
                >
                  {isSimulationRunning ? 'Simulation Running...' : 'Trigger Disturbance Event'}
                </button>
              </div>
              
              <div className="border rounded-md mb-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4">
                  <div>
                    <span className="block text-sm text-gray-600">Calculated RoCoF:</span>
                    <span className={`text-xl font-bold ${
                      rocofValue > 1.0 ? 'text-red-600' : rocofValue > 0.5 ? 'text-amber-600' : 'text-green-600'
                    }`}>
                      {rocofValue} Hz/s
                    </span>
                  </div>
                  
                  <div>
                    <span className="block text-sm text-gray-600">Frequency Nadir:</span>
                    <span className={`text-xl font-bold ${
                      frequencyNadir < 49.5 ? 'text-red-600' : frequencyNadir < 49.7 ? 'text-amber-600' : 'text-green-600'
                    }`}>
                      {frequencyNadir} Hz
                    </span>
                  </div>
                  
                  <div>
                    <span className="block text-sm text-gray-600">Stability Assessment:</span>
                    <span className={`text-xl font-bold ${
                      simulationState === 'unstable' ? 'text-red-600' : 
                      simulationState === 'warning' ? 'text-amber-600' : 'text-green-600'
                    }`}>
                      {simulationState === 'unstable' ? 'Unstable' : 
                       simulationState === 'warning' ? 'Marginally Stable' : 'Stable'}
                    </span>
                  </div>
                </div>
                
                <div className="px-4 pb-4">
                  <p className={`p-3 rounded-md ${
                    simulationState === 'unstable' ? 'bg-red-50 text-red-700' : 
                    simulationState === 'warning' ? 'bg-amber-50 text-amber-700' : 'bg-green-50 text-green-700'
                  }`}>
                    {simulationState === 'unstable' 
                      ? 'This system has critically low inertia for the given disturbance. The high RoCoF would likely trigger protective relays, potentially leading to a cascading failure.' 
                      : simulationState === 'warning'
                        ? 'This system is marginally stable. Additional control measures may be needed to ensure reliable operation.'
                        : 'This system has adequate inertia and would likely remain stable following this disturbance.'}
                  </p>
                </div>
              </div>
              
              <h4 className="font-semibold mb-2">Frequency Response Visualization</h4>
              <div className="h-64 bg-gray-50 p-2 rounded-md border">
                {chartPoints.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartPoints}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="time" 
                        label={{ value: 'Time (seconds)', position: 'insideBottom', offset: -5 }} 
                      />
                      <YAxis 
                        domain={[
                          Math.min(frequencyNadir - 0.2, 49.0), 
                          50.2
                        ]} 
                        label={{ value: 'Frequency (Hz)', angle: -90, position: 'insideLeft' }} 
                      />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="frequency" 
                        stroke={
                          simulationState === 'unstable' ? '#F44336' : 
                          simulationState === 'warning' ? '#FFA726' : '#4CAF50'
                        } 
                        strokeWidth={2}
                        dot={false}
                        isAnimationActive={true}
                      />
                      {/* Reference lines */}
                      <svg>
                        <defs>
                          <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="rgba(244, 67, 54, 0.1)" />
                            <stop offset="100%" stopColor="rgba(244, 67, 54, 0)" />
                          </linearGradient>
                        </defs>
                      </svg>
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-full flex items-center justify-center text-gray-500">
                    Click "Trigger Disturbance Event" to see frequency response
                  </div>
                )}
              </div>
            </div>
            
            <h3 className="text-2xl font-bold mb-4">Frequently Asked Questions</h3>
            
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              {faqs.map((faq, index) => (
                <div key={index} className="mb-4 border-b pb-4 last:border-b-0 last:pb-0">
                  <button
                    className="flex justify-between items-center w-full text-left font-semibold text-blue-900"
                    onClick={() => toggleFaq(index)}
                  >
                    {faq.question}
                    {expandedFaqs.includes(index) ? (
                      <ChevronUp size={20} />
                    ) : (
                      <ChevronDown size={20} />
                    )}
                  </button>
                  <div className={`mt-2 text-gray-700 ${expandedFaqs.includes(index) ? 'block' : 'hidden'}`}>
                    {faq.answer}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Conclusion section - show on all tabs */}
        <div className="mt-12 bg-blue-50 rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold mb-4">A Covenant with the Future</h2>
          
          <p className="text-lg mb-4">
            The intricate technical discussions surrounding grid stability, inertia, RoCoF, and Black Start capabilities ultimately converge on a fundamental human imperative: securing the foundations of modern life for ourselves and for generations to follow.
          </p>
          
          <p className="text-lg mb-4">
            Reliable electricity is not merely a convenience; it is the unseen current that sustains our access to clean water, enables the production and preservation of healthy food, powers our hospitals and schools, connects our communities, and drives economic opportunity.
          </p>
          
          <div className="bg-blue-100 border-l-4 border-blue-500 p-4 mb-6">
            <p className="text-lg text-blue-800">
              "Let us ensure that the legacy we leave is one of a robust, resilient, and reliable energy system – a foundation upon which our grandchildren can continue to build a prosperous and sustainable future, secure in the knowledge that the unseen current will continue to flow."
            </p>
          </div>
          
          <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-6">
            <div className="flex-1">
              <h4 className="font-bold mb-2 flex items-center">
                <span className="w-8 h-8 bg-blue-200 rounded-full flex items-center justify-center text-blue-800 mr-2">1</span>
                Foresight
              </h4>
              <p className="pl-10">
                We must move beyond reactive measures and embrace proactive planning and investment, anticipating future grid needs before crises emerge.
              </p>
            </div>
            
            <div className="flex-1">
              <h4 className="font-bold mb-2 flex items-center">
                <span className="w-8 h-8 bg-blue-200 rounded-full flex items-center justify-center text-blue-800 mr-2">2</span>
                Innovation
              </h4>
              <p className="pl-10">
                Continued research, development, and deployment of stabilizing technologies are essential to managing the transition successfully.
              </p>
            </div>
            
            <div className="flex-1">
              <h4 className="font-bold mb-2 flex items-center">
                <span className="w-8 h-8 bg-blue-200 rounded-full flex items-center justify-center text-blue-800 mr-2">3</span>
                Stewardship
              </h4>
              <p className="pl-10">
                Managing this vital infrastructure demands collaboration among all stakeholders and a profound sense of responsibility.
              </p>
            </div>
          </div>
        </div>
      </main>
      
      <footer className="bg-gray-800 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold mb-4">About the Author</h3>
              <p className="mb-2">
                J. McKenney has over 25 years of experience in power systems engineering and grid stability analysis. Their work in Australia following the 2016 South Australia blackout and recent presentations at the Chicago Grid Stability Conference have focused on the challenges of maintaining reliability in systems with high renewable penetration.
              </p>
              <p>
                This analysis reflects insights from industry experience, academic research, and practical field work across three continents.
              </p>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold mb-4">References & Resources</h3>
              <ul className="space-y-2">
                <li>NERC PRC-029-1 Standard for Inverter-Based Resource Performance</li>
                <li>IEEE Standard 2800-2022 for Interconnection and Interoperability of IBRs</li>
                <li>ENTSO-E Frequency Quality Standards and Inertia Requirements</li>
                <li>2025 European Power Outage Analysis, ENTSO-E</li>
                <li>NREL Grid-Forming Technology Research Roadmap</li>
                <li>UNIFI Consortium for Grid-Forming Inverters</li>
                <li>UK ESO Black Start Strategy and Distributed Re-Start Initiative</li>
              </ul>
            </div>
          </div>
          
          <div className="mt-8 pt-6 border-t border-gray-700 text-center">
            <p>&copy; 2025 J. McKenney. All rights reserved.</p>
            <p className="text-gray-400 text-sm mt-2">
              Published May 7, 2025 | Last updated: May 7, 2025
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default GridStabilityExplorer;
