// src/components/Calendar.js

import React, { useState } from 'react';
import Calendar from 'react-calendar';
import './calendar.css'; // Import your custom styles

const MyCalendar = () => {
  const [date, setDate] = useState(new Date()); // Current selected date

  const isOutsideMonth = (tileDate, activeDate) => {
    // Check if the tileDate is in the same month as the active date
    return tileDate.getMonth() !== activeDate.getMonth() || tileDate.getFullYear() !== activeDate.getFullYear();
  };

  return (
    <div>
      <Calendar
        onChange={setDate} // Update the selected date
        value={date}
        tileClassName={({ date: tileDate, view }) => {
          if (view === 'month') {
            // Highlight today's date
            if (tileDate.toDateString() === new Date().toDateString()) {
              return 'highlight-today';
            }

            // Fade out days outside the active month
            if (isOutsideMonth(tileDate, date)) {
              return 'fade-out';
            }
          }
          return null;
        }}
      />
    </div>
  );
};

export default MyCalendar;
