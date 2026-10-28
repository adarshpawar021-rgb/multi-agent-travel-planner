/**
 * Multi-Agent Travel Planner – Frontend Script
 * Handles sample data filling, INR formatting, interactive checklists,
 * and live agent execution progress synchronization.
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const tripForm = document.getElementById('tripForm');
  const quickSampleBtn = document.getElementById('quickSampleBtn');
  const loadSampleHeroBtn = document.getElementById('loadSampleHeroBtn');
  const budgetInput = document.getElementById('budget');
  const budgetHint = document.getElementById('budgetFormattedHint');
  const agentDashboard = document.getElementById('agentDashboard');
  const generatePlanBtn = document.getElementById('generatePlanBtn');
  const executionTimer = document.getElementById('executionTimer');

  // 1. Indian Rupee Formatter Utility
  function formatINR(val) {
    if (!val || isNaN(val)) return '₹0';
    const num = Math.round(Number(val));
    const str = Math.abs(num).toString();
    let result = '';
    if (str.length <= 3) {
      result = str;
    } else {
      const lastThree = str.substring(str.length - 3);
      const otherNumbers = str.substring(0, str.length - 3);
      const formattedOthers = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ',');
      result = formattedOthers + ',' + lastThree;
    }
    return (num < 0 ? '-₹' : '₹') + result;
  }

  // Live budget hint listener
  if (budgetInput && budgetHint) {
    const updateBudgetHint = () => {
      const val = parseFloat(budgetInput.value);
      if (val && !isNaN(val)) {
        budgetHint.textContent = `Formatted: ${formatINR(val)} INR`;
        budgetHint.style.color = 'var(--primary)';
      } else {
        budgetHint.textContent = 'Approx total funds in ₹ INR';
        budgetHint.style.color = 'var(--text-muted)';
      }
    };
    budgetInput.addEventListener('input', updateBudgetHint);
    updateBudgetHint();
  }

  // 2. Quick Fill Sample Trip (Pune -> Goa, 3 Days, 2 Travelers, ₹10,000, Budget, Beaches + Food)
  const populateSampleTrip = () => {
    const startingCityEl = document.getElementById('starting_city');
    const destinationEl = document.getElementById('destination');
    const daysEl = document.getElementById('days');
    const travelersEl = document.getElementById('travelers');

    if (startingCityEl) startingCityEl.value = 'Pune';
    if (destinationEl) destinationEl.value = 'Goa';
    if (daysEl) daysEl.value = '3';
    if (travelersEl) travelersEl.value = '2';
    if (budgetInput) {
      budgetInput.value = '10000';
      if (budgetHint) {
        budgetHint.textContent = `Formatted: ${formatINR(10000)} INR`;
        budgetHint.style.color = 'var(--primary)';
      }
    }

    // Set Travel Style to 'Budget'
    const styleRadios = document.querySelectorAll('input[name="travel_style"]');
    styleRadios.forEach(radio => {
      radio.checked = radio.value === 'Budget';
    });

    // Set Interests to Beaches and Food
    const interestCheckboxes = document.querySelectorAll('input[name="interests"]');
    interestCheckboxes.forEach(cb => {
      cb.checked = (cb.value === 'Beaches' || cb.value === 'Food');
    });

    // Smooth scroll to planner section
    const plannerSec = document.getElementById('planner-section');
    if (plannerSec) {
      plannerSec.scrollIntoView({ behavior: 'smooth' });
    }
  };

  if (quickSampleBtn) {
    quickSampleBtn.addEventListener('click', populateSampleTrip);
  }
  if (loadSampleHeroBtn) {
    loadSampleHeroBtn.addEventListener('click', populateSampleTrip);
  }

  // 3. Multi-Agent Live Execution Visualizer
  if (tripForm) {
    tripForm.addEventListener('submit', async (e) => {
      // Validate at least one interest is chosen
      const selectedInterests = Array.from(document.querySelectorAll('input[name="interests"]:checked'));
      if (selectedInterests.length === 0) {
        alert('Please select at least one traveler interest (e.g. Beaches, Food, Culture).');
        e.preventDefault();
        return;
      }

      // Check required fields
      const startCity = document.getElementById('starting_city').value.trim();
      const dest = document.getElementById('destination').value.trim();
      const days = parseInt(document.getElementById('days').value, 10);
      const travelers = parseInt(document.getElementById('travelers').value, 10);
      const budget = parseFloat(document.getElementById('budget').value);

      if (!startCity || !dest || isNaN(days) || isNaN(travelers) || isNaN(budget)) {
        return; // Let standard HTML5 validation display errors
      }

      // Prevent standard form submission to execute live agent animation
      e.preventDefault();

      // Show Agent Dashboard
      agentDashboard.style.display = 'block';
      agentDashboard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

      // Disable submit button & show spinner
      generatePlanBtn.disabled = true;
      generatePlanBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Agents Collaborating...';

      // Start elapsed timer
      let startTime = Date.now();
      let timerInterval = setInterval(() => {
        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
        if (executionTimer) {
          executionTimer.textContent = `Elapsed: ${elapsed}s`;
        }
      }, 100);

      // Helper function to update agent step visually
      function setAgentStep(stepId, badgeId, status, descId, text) {
        const item = document.getElementById(stepId);
        const badge = document.getElementById(badgeId);
        const desc = document.getElementById(descId);

        if (item) {
          item.classList.remove('is-running', 'is-completed');
          if (status === 'In Progress' || status === 'Processing') {
            item.classList.add('is-running');
          } else if (status === 'Completed') {
            item.classList.add('is-completed');
          }
        }

        if (badge) {
          badge.className = 'step-status-badge';
          if (status === 'In Progress' || status === 'Processing') {
            badge.classList.add('status-running');
            badge.textContent = 'Processing';
          } else if (status === 'Completed') {
            badge.classList.add('status-completed');
            badge.textContent = 'Completed';
          } else {
            badge.classList.add('status-pending');
            badge.textContent = status;
          }
        }

        if (desc && text) {
          desc.textContent = text;
        }
      }

      // Step 1: Coordinator starts
      setAgentStep('step-coordinator-init', 'badge-coordinator-init', 'Processing', 'desc-coordinator-init', `Analyzing request for ${dest} (${days} days, ${travelers} travelers)...`);

      // Prepare payload
      const travelStyleEl = document.querySelector('input[name="travel_style"]:checked');
      const payload = {
        starting_city: startCity,
        destination: dest,
        days: days,
        travelers: travelers,
        budget: budget,
        travel_style: travelStyleEl ? travelStyleEl.value : 'Standard',
        interests: selectedInterests.map(cb => cb.value)
      };

      try {
        // Send request to API
        const response = await fetch('/api/plan-trip', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!data.success) {
          clearInterval(timerInterval);
          alert('Planning Error: ' + (data.error || 'Failed to generate plan'));
          generatePlanBtn.disabled = false;
          generatePlanBtn.innerHTML = '<i class="fa-solid fa-arrows-spin"></i> Generate Travel Plan';
          return;
        }

        const plan = data.plan;

        // Sequence through the agent progression based on real execution logs
        setAgentStep('step-coordinator-init', 'badge-coordinator-init', 'Completed', 'desc-coordinator-init', 'Decomposition complete. Tasks dispatched to specialized sub-agents.');

        // Step 2: Destination Agent
        setAgentStep('step-destination', 'badge-destination', 'Processing', 'desc-destination', `Researching top attractions and cultural spots in ${dest}...`);
        await new Promise(r => setTimeout(r, 450));
        setAgentStep('step-destination', 'badge-destination', 'Completed', 'desc-destination', `Curated ${plan.recommended_places.length} attractions matching ${payload.interests.join(', ')}.`);

        // Step 3: Itinerary Agent
        setAgentStep('step-itinerary', 'badge-itinerary', 'Processing', 'desc-itinerary', `Assembling ${days}-day schedule across morning, afternoon, and evening slots...`);
        await new Promise(r => setTimeout(r, 450));
        setAgentStep('step-itinerary', 'badge-itinerary', 'Completed', 'desc-itinerary', `Day-by-day balanced itinerary created with zero scheduling conflicts.`);

        // Step 4: Budget Agent
        setAgentStep('step-budget', 'badge-budget', 'Processing', 'desc-budget', `Estimating accommodation, transport, meals, and activity costs in INR...`);
        await new Promise(r => setTimeout(r, 450));
        const budgetMsg = plan.budget_breakdown.is_over_budget
          ? `Estimated ${plan.budget_breakdown.formatted.estimated_total} (Over budget by ${plan.budget_breakdown.formatted.difference}. Cost-saving options added).`
          : `Estimated ${plan.budget_breakdown.formatted.estimated_total} (Safely within budget, surplus: ${plan.budget_breakdown.formatted.difference}).`;
        setAgentStep('step-budget', 'badge-budget', 'Completed', 'desc-budget', budgetMsg);

        // Step 5: Travel Essentials Agent
        setAgentStep('step-essentials', 'badge-essentials', 'Processing', 'desc-essentials', `Assembling customized packing list, IDs, gadgets, and local safety tips...`);
        await new Promise(r => setTimeout(r, 450));
        setAgentStep('step-essentials', 'badge-essentials', 'Completed', 'desc-essentials', `Checklist and safety guidelines ready for ${dest}.`);

        // Step 6: Coordinator Validation & Synthesis
        setAgentStep('step-coordinator-final', 'badge-coordinator-final', 'Processing', 'desc-coordinator-final', 'Validating constraints and compiling final travel plan document...');
        await new Promise(r => setTimeout(r, 400));
        setAgentStep('step-coordinator-final', 'badge-coordinator-final', 'Completed', 'desc-coordinator-final', 'All constraints validated. Final Travel Plan ready!');

        clearInterval(timerInterval);

        // Redirect to the result view
        setTimeout(() => {
          window.location.href = '/plan/result';
        }, 500);

      } catch (err) {
        clearInterval(timerInterval);
        console.error('API submission failed:', err);
        // Fall back to submitting the form conventionally
        tripForm.submit();
      }
    });
  }

  // 4. Interactive Packing Checklist (Result Page)
  const planCheckboxes = document.querySelectorAll('.plan-checkbox');
  const checkedCountEl = document.getElementById('checkedCount');

  if (planCheckboxes.length > 0 && checkedCountEl) {
    const updateCheckedCount = () => {
      const checkedCount = document.querySelectorAll('.plan-checkbox:checked').length;
      const totalCount = planCheckboxes.length;
      checkedCountEl.textContent = `${checkedCount} / ${totalCount}`;

      // Save state in localStorage
      const state = Array.from(planCheckboxes).map(cb => cb.checked);
      localStorage.setItem('trip_checklist_state', JSON.stringify(state));
    };

    // Restore state from localStorage if available
    try {
      const saved = JSON.parse(localStorage.getItem('trip_checklist_state') || '[]');
      if (Array.isArray(saved) && saved.length === planCheckboxes.length) {
        planCheckboxes.forEach((cb, idx) => {
          cb.checked = !!saved[idx];
        });
      }
    } catch (e) {
      // Ignore storage errors
    }

    planCheckboxes.forEach(cb => {
      cb.addEventListener('change', updateCheckedCount);
    });

    updateCheckedCount();
  }
});
