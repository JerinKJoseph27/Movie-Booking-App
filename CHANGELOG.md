# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-14

### Added
- Initial release of CinemaMax Movie Booking System
- Multi-movie browsing interface with poster display
- Interactive seat selection with real-time availability
- Customer information validation (name and Indian phone numbers)
- Unique booking ID generation system
- Professional PDF ticket generation with ReportLab
- MySQL database integration for persistent storage
- Responsive web design for mobile and desktop
- Theatre seat auto-generation (14 rows × 20 seats)
- Booking confirmation page with download option
- Comprehensive README with setup instructions
- MIT License

### Features
- **Movies Management**: Support for multiple movies with individual seat layouts
- **Seat Selection**: Visual seat map showing available (green) and booked (red) seats
- **Validation**: Server-side validation for names and phone numbers
- **PDF Tickets**: Branded PDF tickets with booking details and QR code placeholder
- **Dynamic Pricing**: ₹150 per seat pricing system
- **Database**: Three-table schema (movies, seats, bookings)

### Technical Stack
- Python 3.8+ with Flask framework
- MySQL 8.0+ database
- ReportLab for PDF generation
- HTML5/CSS3/JavaScript frontend
- Responsive design with gradient themes

### Documentation
- README.md with comprehensive setup guide
- QUICK_START.md for rapid deployment
- CONTRIBUTING.md for developer guidelines
- SECURITY_CHECKLIST.md for deployment safety
- db_config.sql with database schema

## [Unreleased]

### Planned Features
- Payment gateway integration
- Email notifications for bookings
- Admin panel for movie management
- User authentication and login
- Booking history and management
- Multiple show timings per movie
- Different seat categories and pricing
- Reviews and ratings system
- Movie search and filtering
- Mobile app version

### Known Issues
- QR code in PDF ticket is placeholder only
- No email confirmation system
- Hardcoded show time in tickets
- Single screen support only
- No booking cancellation feature

## Version History

- **v1.0.0** - Initial public release (January 2026)

---

## Types of Changes

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities
