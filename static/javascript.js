import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css';
import 'tippy.js/themes/light.css';



document.addEventListener("DOMContentLoaded", function() {
  const tour = new Shepherd.Tour({
    defaultStepOptions: {
      classes: 'shadow-md bg-purple-600 text-white', // Tailwind-based styling
      scrollTo: { behavior: 'smooth', block: 'center' },
      cancelIcon: {
        enabled: true
      },
      buttons: [
        {
          text: 'Next',
          action: Shepherd.next
        }
      ]
    }
  });

  // Step 1: Add Note Button
  tour.addStep({
    title: 'Add a New Note',
    text: 'Click here to add a new note to your collection.',
    attachTo: {
      element: "bg-orange-200 hover:bg-orange-700 text-white font-semibold py-2 px-4 rounded mb-4", // The CSS class for your Add Note button
      on: 'bottom' // Position of the tooltip relative to the element
    },
    buttons: [
      {
        text: 'Next',
        action: tour.next
      }
    ]
  });

  // Step 2: My Notes Navbar Link
  tour.addStep({
    title: 'View Your Notes',
    text: 'This is where you can access all your saved notes.',
    attachTo: {
      element:"text-lg text-gray-800 hover:text-gray-600", // The CSS class for the My Notes link
      on: 'bottom'
    },
    buttons: [
      {
        text: 'Back',
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      }
    ]
  });

  // Optionally start the tour automatically when the page loads
  tour.start();
});

