import { defineCollection, z } from 'astro:content';

const tutorials = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    duration: z.string(),
    difficulty: z.enum(['入门', '进阶', '实战']),
    outcome: z.string(),
    order: z.number().optional(),
  }),
});

export const collections = { tutorials };
