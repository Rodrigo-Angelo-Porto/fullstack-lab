SELECT users.name
FROM users
JOIN registrations ON users.id = registrations.user_id
WHERE registrations.event_id = :event_id
ORDER BY users.name;
