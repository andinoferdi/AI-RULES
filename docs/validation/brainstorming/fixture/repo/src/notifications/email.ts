import { ServerClient } from "postmark";

const client = new ServerClient(process.env.POSTMARK_TOKEN ?? "");

export async function sendEmail(to: string, template: string, vars: Record<string, unknown>) {
  await client.sendEmailWithTemplate({
    From: "desk@northsidetools.org",
    To: to,
    TemplateAlias: template,
    TemplateModel: vars,
  });
}
