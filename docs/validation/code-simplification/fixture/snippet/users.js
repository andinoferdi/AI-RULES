async function loadUser(service, id) {
  return await service.findById(id);
}

function displayName(user) {
  let name;
  if (user.nickname) {
    name = user.nickname;
  } else {
    name = user.firstName + " " + user.lastName;
  }
  return name;
}

function roleBadge(user) {
  return user.isAdmin ? "admin" : user.isModerator ? "moderator" : user.isBanned ? "banned" : "member";
}

function activeEmails(users) {
  const result = [];
  for (let i = 0; i < users.length; i++) {
    const u = users[i];
    if (u.active === true) {
      if (u.email != null) {
        result.push(u.email.trim().toLowerCase());
      }
    }
  }
  return result;
}

function summarize(users) {
  const data = {};
  for (const u of users) {
    const badge = roleBadge(u);
    if (data[badge] === undefined) {
      data[badge] = 0;
    }
    data[badge] = data[badge] + 1;
  }
  return data;
}

module.exports = { loadUser, displayName, roleBadge, activeEmails, summarize };
