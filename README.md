# Fly.io Flask Starter App

using supabase for auth and db

continually deploy to fly.io with github action



# TODO. actually write these instructions...
### Deploying Instructions

install fly cli

run `fly launch` from project root

`fly secrets set SUPABASE_URL=<supabase-url>` # `fly secrets set SUPABASE_KEY=<supabase-key>`

Create supabase project and copy url and key and save

actually not sure if pushing to github will work if thhere isn't already an app.
(maybe look into a launch/deploy github automation??)
